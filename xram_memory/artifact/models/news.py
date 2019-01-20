from django.core.files.base import ContentFile
from django.core.validators import URLValidator

from pathlib import Path

from django.template.defaultfilters import slugify
from django.conf import settings
import datetime
from ..news_fetcher import NewsFetcher
from .documents import PDFDocument, ImageDocument

from xram_memory.logger.decorators import log_process
from xram_memory.taxonomy.models import Keyword
from .artifact import Artifact

import django_rq
import redis


from django.db import models
from django_rq import job


class News(Artifact):
    '''
    Uma notícia da Internet
    '''
    url = models.URLField(
        max_length=255, help_text="Endereço original da notícia",
        verbose_name="Endereço", unique=True, null=False, validators=[URLValidator])
    archived_news_url = models.URLField(
        max_length=255, help_text="Endereço da notícia no <a href='https://archive.org/'>Archive.org</a>",
        verbose_name="Endereço no Internet Archive", null=True, blank=True)
    # TODO: fazer um relacionamento com um artefato do tipo imagem
    authors = models.TextField(
        blank=True, verbose_name="Autores", help_text='Nomes dos autores, separados por vírgula')
    body = models.TextField(
        blank=True, verbose_name="Texto da notícia", help_text="Texto integral da notícia")
    published_date = models.DateTimeField(verbose_name='Data de publicação', blank=True, null=True,
                                          help_text='Data em que a notícia foi publicada')

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"

    def save(self, *args, **kwargs):
        if not self.url:
            raise ValueError(
                "Você precisa definir um endereço para a notícia.")

        set_basic_info = getattr(
            self, '_set_basic_info', self.pk is None)
        fetch_archived_url = getattr(
            self, '_fetch_archived_url', self.pk is None)
        add_pdf_capture = getattr(
            self, '_add_pdf_capture', self.pk is None)

        if set_basic_info:
            self.set_basic_info()

        if fetch_archived_url:
            self.fetch_archived_url()

        # Salve a notícia
        super(News, self).save(*args, **kwargs)

        if add_pdf_capture:
            # TODO: fazer um decorador, abstrair o padrão abaixo de tentar executar assíncronamente mas executar
            # síncronamente se o redis não estiver disponível. Logar em caso de erro.
            try:
                django_rq.get_queue().get_job_ids()
            except redis.exceptions.ConnectionError:
                self.add_pdf_capture()
            else:
                self.add_pdf_capture.delay()
        self.add_fetched_keywords()
        if hasattr(self, '_image') and len(self._image) > 0:
            self.add_fetched_image()

    @property
    def has_basic_info(self):
        '''
        Retorna verdadeiro se ao menos um dos campos básicos estiver preenchido
        TODO: acrescentar campos de relacionamento e não verificar eles se o objeto for novo.
        '''
        return (bool(self.title) or bool(self.teaser) or bool(self.body) or bool(self.authors) or
                bool(self.published_date))

    @property
    def has_pdf_capture(self):
        '''
        Retorna verdadeiro se houver ao menos uma captura em pdf para esta notícia
        '''
        if self.pk is None:
            return False
        else:
            return bool(self.pdf_captures.count() > 0)

    @log_process(operation="verificar por uma versão no archive.org", object_type="Notícia")
    def fetch_archived_url(self):
        '''
        Verifica se existe adiciona a URL de uma versão arquivada desta notícia no `Internet Archive`
        '''
        self.archived_news_url = NewsFetcher.fetch_archived_url(self.url)

    @log_process(operation="buscar informações básicas", object_type="Notícia")
    def set_basic_info(self):
        '''
        Abre a página da notícia e tenta inferir e definir suas informações básicas
        '''
        basic_info = NewsFetcher.fetch_basic_info(self.url)
        for prop, value in basic_info.items():
            if prop == 'keywords':
                setattr(self, '_keywords', value)
            elif prop == 'image':
                setattr(self, '_image', value)
            else:
                setattr(self, prop, value)

    @job
    @log_process(operation="adicionar uma captura em formato PDF", object_type="Notícia")
    def add_pdf_capture(self):
        '''
        Captura a notícia em formato para impressão e em PDF
        '''
        pdf_content = NewsFetcher.get_pdf_capture(
            self.url, settings.PDF_ARTIFACT_DIR)

        uniq_filename = (
            str(datetime.datetime.now().date()) + '_' +
            str(datetime.datetime.now().time()).replace(':', '.') + '.pdf'
        )

        pdf_path = settings.PDF_ARTIFACT_DIR + uniq_filename
        file_pdf_path = str(Path(settings.MEDIA_ROOT, pdf_path))

        pdf_file = ContentFile(pdf_content, uniq_filename)

        pdf_document = PDFDocument.objects.create(
            pdf_file=pdf_file, is_user_object=False)

        NewsPDFCapture.objects.create(
            news=self, pdf_document=pdf_document)

    def add_fetched_keywords(self):
        # TODO: fortificar esse código, último except pode falhar
        if hasattr(self, '_keywords') and len(self._keywords) > 0:
            for keyword in self._keywords:
                # TODO: refatorar para usar um objeto Q?
                try:
                    # tente achar a palavra-chave pelo nome
                    db_keyword = Keyword.objects.get(name=keyword)
                    self.keywords.add(db_keyword)
                except Keyword.DoesNotExist:
                    # caso não consiga, tente achar pela slug
                    try:
                        db_keyword = Keyword.objects.get(
                            slug=slugify(keyword))
                        self.keywords.add(db_keyword)
                    # caso não ache, crie uma palavra-chave utilizando o usuário que modificou esta notícia
                    except Keyword.DoesNotExist:
                        self.keywords.create(name=keyword, slug=slugify(keyword), created_by=self.modified_by,
                                             modified_by=self.modified_by)

    @log_process(operation="baixar uma imagem", object_type="Notícia")
    def add_fetched_image(self):
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
            image_path = settings.IMAGE_ARTIFACT_DIR + uniq_filename
            file_image_path = str(Path(settings.MEDIA_ROOT, image_path))

            image_contents = NewsFetcher.fetch_image(self._image)
            image_file = ContentFile(image_contents, uniq_filename)

            image_document = ImageDocument.objects.create(
                image_file=image_file, is_user_object=False)
            NewsImageCapture.objects.create(
                image_document=image_document, original_url=self._image, news=self)


class NewsPDFCapture(models.Model):
    '''
    Um documento PDF para uma captura de página de uma notícia
    '''
    news = models.ForeignKey(
        News, on_delete=models.SET_NULL, null=True, related_name="pdf_captures")
    pdf_document = models.OneToOneField(PDFDocument, on_delete=models.CASCADE)
    pdf_capture_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de captura', blank=True, null=True,
                                            help_text='Data desta captura')

    class Meta:
        verbose_name = "Captura de Notícia em PDF"
        verbose_name_plural = "Capturas de Notícia em PDF"


class NewsImageCapture(models.Model):
    '''
    Um documento PDF para uma captura de página de uma notícia
    '''
    news = models.OneToOneField(
        News, on_delete=models.SET_NULL, null=True, related_name="image_capture")
    image_document = models.OneToOneField(
        ImageDocument, on_delete=models.CASCADE)
    image_capture_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de captura', blank=True, null=True,
                                              help_text='Data desta captura')
    original_url = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Imagem capturada em Notícias"
        verbose_name_plural = "Imagens capturadas em Notícias"
