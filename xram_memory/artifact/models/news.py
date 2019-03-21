from xram_memory.artifact.models import Artifact, Newspaper
from xram_memory.artifact import tasks as background_tasks
from django.db import models, transaction, IntegrityError
from xram_memory.artifact.news_fetcher import NewsFetcher
from xram_memory.logger.decorators import log_process
from filer.utils.generate_filename import randomized
from django.template.defaultfilters import slugify
from easy_thumbnails.files import get_thumbnailer
from django.core.files import File as DjangoFile
from django.core.validators import URLValidator
from xram_memory.taxonomy.models import Keyword
from django.core.files.base import ContentFile
from filer.fields.image import FilerImageField
from boltons.cacheutils import cachedproperty
from filer.fields.file import FilerFileField
from django.db.transaction import on_commit
from filer.models.imagemodels import Image
from filer.models import File as FilerFile
from filer.models import File, Folder
from django.conf import settings
from django.db.models import Q
from celery import group
from pathlib import Path
import tempfile
import datetime
import urllib
import os


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
        null=True,
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
            self.set_web_title()

        # salva a notícia
        super().save(*args, **kwargs)

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
    def set_web_title(self):
        """
        Pega o título para a página desta notícia.
        """
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

        import hashlib
        uniq_filename = (
            str(datetime.datetime.now().date()) + '_' +
            str(datetime.datetime.now().time()).replace(':', '.')
        )
        filename = hashlib.md5(uniq_filename.encode(
            'utf-8')).hexdigest() + '.pdf'

        with NewsFetcher.get_pdf_capture(self.url) as fd:
            django_file = DjangoFile(fd, name=filename)
            with transaction.atomic():
                folder, _, = Folder.objects.get_or_create(
                    name="Capturas de notícias em PDF")
                new_pdf_document = FilerFile(file=django_file, name=filename,
                                             original_filename=filename,
                                             folder=folder,  owner=self.modified_by,
                                             is_public=True)
                # Reaproveite um arquivo já existente, com base no seu hash, de forma que um arquivo possa ser utilizado
                # várias vezes, por várias capturas. Ao que parece, contudo o wkhtmltopdf sempre gera arquivos
                # diferentes...
                try:
                    pdf_document = FilerFile.objects.get(
                        sha1=new_pdf_document.sha1)
                except FilerFile.DoesNotExist:
                    new_pdf_document.save()
                    pdf_document = new_pdf_document

                NewsPDFCapture.objects.create(
                    news=self, pdf_document=pdf_document)

    @log_process(operation="adicionar palavras-chave", object_type="Notícia")
    def add_fetched_keywords(self):
        """
        Para cada uma das palavras-chave descobertas por set_basic_info(), crie uma palavra-chave no
        banco de dados e associe ela a esta notícia
        """
        if hasattr(self, '_keywords') and len(self._keywords) > 0:
            keywords = []
            for keyword in self._keywords:
                try:
                    # tente achar a palavra-chave pelo nome ou pela slug
                    keywords.append(Keyword.objects.get(name=keyword))
                except Keyword.DoesNotExist:
                    try:
                        keywords.append(Keyword.objects.create(name=keyword, created_by=self.modified_by,
                                                               modified_by=self.modified_by))
                    except IntegrityError:
                        pass
            if len(keywords):
                self.keywords.add(*keywords)

    @log_process(operation="baixar uma imagem", object_type="Notícia")
    def add_fetched_image(self):
        """
        Com base na url da imagem descoberta por set_basic_info(), baixa a imagem e arquivo e o
        associa à uma nova captura de imagem de notícia (NewsImageCapture).
        """
        original_filename = Path(self._image).name
        original_extension = Path(self._image).suffix
        import hashlib
        filename = hashlib.md5(self._image.encode(
            'utf-8')).hexdigest() + original_extension

        with NewsFetcher.fetch_image(self._image) as fd:
            django_file = DjangoFile(fd, name=filename)
            with transaction.atomic():
                # tente apagar todas as imagens associadas a esta notícia, pois só pode haver uma
                try:
                    captures_for_this_news = self.image_capture
                    captures_for_this_news.delete()
                except (NewsImageCapture.DoesNotExist):
                    pass  # Não existem imagens associadas a esta notícia
                folder, _, = Folder.objects.get_or_create(
                    name="Imagens de notícias")

                new_image_document = Image(file=django_file, name=filename,
                                           original_filename=original_filename,
                                           folder=folder,  owner=self.modified_by,
                                           is_public=True)
                # Reaproveite um arquivo já existente, com base no seu hash, de forma que um arquivo possa ser utilizado
                # várias vezes, por várias capturas.
                try:
                    image_document = Image.objects.get(
                        sha1=new_image_document.sha1)
                except Image.DoesNotExist:
                    new_image_document.save()
                    image_document = new_image_document

                NewsImageCapture.objects.create(
                    image_document=image_document, original_url=self._image, news=self)

    @cachedproperty
    def image_capture_indexing(self):
        """
        Retorna a url para uma captura de imagem desta notícia, se existente.
        """
        try:
            if self.image_capture:
                url = get_thumbnailer(self.image_capture.image_document.file)[
                    'image_capture'].url
                return url
        except:
            return None

    @cachedproperty
    def thumbnail(self):
        """
        Retorna a url para uma miniatura de uma captura de página desta notícia, se existente.
        """
        try:
            if self.image_capture:
                url = get_thumbnailer(self.image_capture.image_document.file)[
                    'thumbnail'].url
                return url
        except:
            return None

    @property
    def published_year(self):
        """
        Retorna o ano de publicação desta notícia.
        """
        try:
            # Tente retornar o ano da data de publicação
            return self.published_date.timetuple()[0]
        except AttributeError:
            try:
                # Ou ao menos o ano data de criação dessa Notícia no sistema
                return self.created_at.timetuple()[0]
            except AttributeError:
                return None


class NewsPDFCapture(models.Model):
    """
    Um captura que associa um arquivo em PDF com uma Notícia (News)
    """
    news = models.ForeignKey(
        News,
        verbose_name="Notícia",
        on_delete=models.CASCADE,
        null=True,
        related_name="pdf_captures",
    )
    pdf_document = FilerFileField(
        verbose_name="Documento PDF",
        on_delete=models.CASCADE,
        related_name="pdf_captures"
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
        try:
            return "Captura em PDF de \"{}\"".format(self.news.url)
        except AttributeError:
            return "Captura em PDF de notícia"


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
    image_document = FilerImageField(
        verbose_name="Documento de imagem",
        on_delete=models.CASCADE,
        related_name="image_capture"
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
    )

    class Meta:
        verbose_name = "Imagem de Notícia"
        verbose_name_plural = "Imagens de Notícias"

    def __str__(self):
        try:
            return "Imagem principal de \"{}\"".format(self.news.url)
        except AttributeError:
            return "Imagem principal de notícia"
