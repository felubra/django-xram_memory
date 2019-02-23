import urllib
import datetime
from pathlib import Path

from celery import group
from django.conf import settings
from django.db.models import Q
from django.db import models, transaction
from django.db.transaction import on_commit
from django.core.files.base import ContentFile
from django.core.validators import URLValidator
from easy_thumbnails.files import get_thumbnailer
from django.template.defaultfilters import slugify

from xram_memory.artifact.models import Artifact, Document, Newspaper
from xram_memory.artifact.news_fetcher import NewsFetcher
from xram_memory.artifact import tasks as background_tasks
from xram_memory.logger.decorators import log_process
from xram_memory.taxonomy.models import Keyword


class News(Artifact):
    """
    Uma notícia capturada da Internet

    Este modelo gerará um artefato do tipo notícia e possivelmente outros artefatos como uma captura
    de página (NewsPDFCapture) e uma imagem associada a notícia (NewsImageCapture).
    """
    url = models.URLField(
        verbose_name="Endereço",
        help_text="Endereço original da notícia",
        max_length=255,
        unique=True,
        null=False,
        validators=[URLValidator],
    )
    # TODO: adicionar validador de URL
    archived_news_url = models.URLField(
        verbose_name="Endereço no Internet Archive",
        help_text="Endereço da notícia no <a href='https://archive.org/'>Archive.org</a>",
        max_length=255,
        null=True,
        blank=True,
    )
    authors = models.TextField(
        verbose_name="Autores",
        help_text='Nomes dos autores, separados por vírgula',
        blank=True,
    )
    body = models.TextField(
        verbose_name="Texto da notícia",
        help_text="Texto integral da notícia",
        blank=True,
    )
    published_date = models.DateTimeField(
        verbose_name='Data de publicação',
        help_text='Data em que a notícia foi publicada',
        blank=True,
        null=True,
    )

    language = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        default='pt',
    )

    newspaper = models.ForeignKey(
        Newspaper,
        null=True,
        on_delete=models.SET_NULL,
        related_name='news'
    )

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"

    def save(self, *args, **kwargs):
        """
        Faz uma validação básica, invoca os mecanismos de preenchimento de dados da notícia, agenda
        jobs e salva a notícia.
        """
        if not self.url:
            raise ValueError(
                "Você precisa definir um endereço para a notícia.")

        if not self.title:
            self.fetch_web_title()

        base_url = "{uri.scheme}://{uri.netloc}".format(
            uri=urllib.parse.urlsplit(self.url))
        newspaper_created = False
        try:
            if not self.newspaper and not getattr(self, '_inside_job', None):
                try:
                    newspaper = Newspaper.objects.get(url=base_url)
                    self.newspaper = newspaper
                except Newspaper.DoesNotExist:
                    raise
        except Newspaper.DoesNotExist:
            # crie um jornal (newspaper ) básico agora
            newspaper = Newspaper.objects.create(
                title=base_url,
                url=base_url,
                created_by=self.created_by,
                modified_by=self.modified_by
            )
            self.newspaper = newspaper
            newspaper_created = True
        except:
            self.newspaper = None

        # recebe os atributos do formulário de edição ou define padrões se ausentes
        set_basic_info = getattr(
            self, '_set_basic_info', self.pk is None)
        fetch_archived_url = getattr(
            self, '_fetch_archived_url', self.pk is None)
        add_pdf_capture = getattr(
            self, '_add_pdf_capture', self.pk is None)

        # salva a notícia
        super().save(*args, **kwargs)

        def schedule_tasks(news_id, newspaper_id=None):
            tasks = []
            tasks.append(background_tasks.add_additional_info.s(
                news_id, set_basic_info, fetch_archived_url, add_pdf_capture))
            if newspaper_id:
                tasks.append(
                    background_tasks.newspaper_set_basic_info.s(newspaper_id))
            group(*tasks).apply_async()

        # não entre em loop infinito
        if not getattr(self, '_inside_job', None):
            on_commit(lambda: schedule_tasks(
                self.pk, self.newspaper.pk if self.newspaper and newspaper_created else None))

    @property
    def has_basic_info(self):
        """
        Indica se esta notícia tem ao menos alguns campos preenchidos, ou seja, informações básicas.
        TODO: acrescentar campos de relacionamento e não verificar eles se o objeto for novo.
        """
        return (bool(self.title) or bool(self.teaser) or bool(self.body) or bool(self.authors) or
                bool(self.published_date))

    @property
    def has_pdf_capture(self):
        """
        Indica se existe ao menos uma captura em pdf associada a esta notícia.
        """
        if self.pk is None:
            return False
        else:
            return bool(self.pdf_captures.count() > 0)

    @log_process(operation="pegar o título", object_type="Notícia")
    def fetch_web_title(self):
        self.title = NewsFetcher.fetch_web_title(self.url)

    @log_process(operation="verificar por uma versão no archive.org", object_type="Notícia")
    def fetch_archived_url(self):
        """
        Verifica se existe e adiciona a URL de uma versão arquivada desta notícia presente no
        `Internet Archive`.
        """
        self.archived_news_url = NewsFetcher.fetch_archived_url(self.url)

    @log_process(operation="buscar informações básicas", object_type="Notícia")
    def set_basic_info(self):
        """
        Abre a página da notícia e tenta inferir e definir suas informações básicas.
        """
        basic_info = NewsFetcher.fetch_basic_info(self.url)
        # preenche os campos do modelo com as informações obtidas e lida com casos especiais
        for prop, value in basic_info.items():
            if prop == 'keywords':
                setattr(self, '_keywords', value)
            elif prop == 'image':
                setattr(self, '_image', value)
            else:
                setattr(self, prop, value)
        return basic_info

    @log_process(operation="adicionar uma captura em formato PDF", object_type="Notícia")
    def add_pdf_capture(self):
        """
        Captura a notícia em formato para impressão e em PDF.
        TODO: salvar e usar diretamente o arquivo, não lidar com um buffer de conteúdo.
        """
        # TODO: checar se o diretório existe, se existem permissões para salvar etc
        # TODO: usar o System check framework
        if not settings.PDF_ARTIFACT_DIR:
            raise ValueError(
                'NewsFetcher: o caminho para onde salvar as páginas não foi definido')

        # pega o conteúdo da página do Fetcher
        pdf_content = NewsFetcher.get_pdf_capture(
            self.url)

        # gera um nome de arquivo único
        # TODO: isso pode ser definido na configuração do FileField?
        uniq_filename = (
            str(datetime.datetime.now().date()) + '_' +
            str(datetime.datetime.now().time()).replace(':', '.') + '.pdf'
        )
        # gera um arquivo com o conteúdo devolvido pelo fetcher
        pdf_file = ContentFile(pdf_content, uniq_filename)
        # cria um novo documento do tipo PDF
        # TODO: adicionar as tags da notícia
        with transaction.atomic():
            pdf_document = Document.objects.create(
                file=pdf_file, is_user_object=False, created_by=self.modified_by,
                modified_by=self.modified_by)
            # cria uma nova captura de página em pdf com o dcumento gerado e associa ela a esta notícia
            NewsPDFCapture.objects.create(
                news=self, pdf_document=pdf_document)
        pdf_file.close()
        del pdf_content

    def add_fetched_keywords(self):
        """
        Para cada uma das palavras-chave descobertas por set_basic_info(), crie uma palavra-chave no
        banco de dados e associe ela a esta notícia
        """
        # TODO: fortificar esse código, último except pode falhar
        if hasattr(self, '_keywords') and len(self._keywords) > 0:
            for keyword in self._keywords:
                # TODO: refatorar para usar um objeto Q?
                try:
                    # tente achar a palavra-chave pelo nome ou pela slug
                        db_keyword = Keyword.objects.get(
                        Q(name=keyword) | Q(slug=slugify(keyword)))
                        self.keywords.add(db_keyword)
                    except Keyword.DoesNotExist:
                    with transaction.atomic():
                        self.keywords.create(name=keyword, created_by=self.modified_by,
                                             modified_by=self.modified_by)

    @log_process(operation="baixar uma imagem", object_type="Notícia")
    def add_fetched_image(self):
        """
        Com base na url da imagem descoberta por set_basic_info(), baixa a imagem e cria uma
        instância dela como documento de artefato (Document) e captura de imagem de notícia
        (NewsImageCapture).
        """
        # TODO: validar se a url da imagem é válida
        # TODO: fortificar esse código, último except pode falhar
        try:
            captured_image = NewsImageCapture.objects.get(
                original_url=self._image)
            self.image_capture = captured_image
        except NewsImageCapture.DoesNotExist:
            original_filename = Path(self._image).name
            uniq_filename = (
                str(datetime.datetime.now().date()) + '_' +
                str(datetime.datetime.now().time()).replace(
                    ':', '.') + original_filename
            )

            image_contents = NewsFetcher.fetch_image(self._image)
            image_file = ContentFile(image_contents, uniq_filename)

            with transaction.atomic():
                image_document = Document.objects.create(
                    file=image_file, is_user_object=False, created_by=self.modified_by,
                    modified_by=self.modified_by)
                NewsImageCapture.objects.create(
                    image_document=image_document, original_url=self._image, news=self)
            image_file.close()
            del image_contents

    @property
    def image_capture_indexing(self):
        try:
            if self.image_capture and self.image_capture.image_document and self.image_capture.image_document.file:
                url = get_thumbnailer(self.image_capture.image_document.file)[
                    'thumbnail'].url
                return url
        except:
            return None


class NewsPDFCapture(models.Model):
    """
    Um captura que associa um documento PDF (PDFDocument) com uma Notícia (News)
    """
    news = models.ForeignKey(
        News,
        verbose_name="Notícia",
        on_delete=models.CASCADE,
        null=True,
        related_name="pdf_captures",
    )
    pdf_document = models.OneToOneField(
        Document,
        verbose_name="Documento PDF",
        on_delete=models.CASCADE,
    )
    pdf_capture_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de captura",
        help_text="Data desta captura",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Captura de Notícia em PDF"
        verbose_name_plural = "Capturas de Notícia em PDF"

    def __str__(self):
        return "Captura em PDF de \"{}\"".format(self.news.url)


class NewsImageCapture(models.Model):
    """
    Um documento PDF para uma captura de página de uma notícia
    """
    news = models.OneToOneField(
        News,
        verbose_name="Notícia",
        on_delete=models.CASCADE,
        null=True,
        related_name="image_capture"
    )
    image_document = models.OneToOneField(
        Document,
        verbose_name="Documento de imagem",
        on_delete=models.CASCADE,
    )
    image_capture_date = models.DateTimeField(
        verbose_name="Data de captura",
        help_text="Data desta captura",
        auto_now_add=True,
        blank=True,
        null=True,
    )
    original_url = models.CharField(
        verbose_name="Endereço original da imagem",
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = "Imagem de Notícia"
        verbose_name_plural = "Imagens de Notícias"

    def __str__(self):
        return "Imagem principal de \"{}\"".format(self.news.url)
