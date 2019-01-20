import requests
import magic
import datetime
import pdfkit
import os
import django_rq
import redis

from timeit import default_timer
from pathlib import Path
from functools import lru_cache

from django.conf import settings
from django_rq import job
from django.db import models
from newspaper import Article
from goose3 import Goose
from goose3.image import Image
from django.template.defaultfilters import slugify

from ..base_models import TraceableEditorialModel
from ..taxonomy.models import Subject, Keyword
from ..logger.decorators import log_process

# TODO: desmembrar este módulo


class Artifact(TraceableEditorialModel):
    # TODO: lidar com a exigência do título
    title = models.CharField(max_length=255, blank=True,
                             help_text="Título", verbose_name="Título")
    teaser = models.TextField(
        help_text="Resumo ou chamada", verbose_name="Resumo ou chamada", blank=True)

    # TODO: adicionar um help_text para `slug`
    slug = models.SlugField(help_text="", verbose_name="Slug", blank=True)

    keywords = models.ManyToManyField(
        Keyword, blank=True, verbose_name="Palavras-chave")
    subjects = models.ManyToManyField(
        Subject, blank=True, verbose_name="Assuntos")

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Artifact, self).save(*args, **kwargs)


class Document(Artifact):
    '''
    Um documento, inserido pelo usuário ou criado pelo sistema
    '''
    mime_type = models.fields.CharField(
        max_length=255, blank=True, editable=False, help_text="Tipo do arquivo")
    file_size = models.fields.PositiveIntegerField(
        default=0, editable=False, help_text="Tamanho do arquivo em bytes")
    file_hash = models.CharField(
        max_length=32, help_text="Hash único do arquivo em MD5")
    aditional_info = models.TextField(
        null=True, editable=False, help_text="Informações adicionais sobre o arquivo (JSON)")
    is_user_object = models.BooleanField(
        default=True, help_text="Indica se o arquivo foi inserido diretamente por um usuário")

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        if not self.aditional_info:
            # TODO: fazer um decorador, abstrair o padrão abaixo de tentar executar assíncronamente mas executar
            # síncronamente se o redis não estiver disponível. Logar em caso de erro.
            try:
                self.extract_aditional_info.delay()
            except:
                self.extract_aditional_info()

    @job
    def extract_aditional_info(self):
        '''
        Com base no mimetype do arquivo, tenta extrair informações adicionais e salvá-las serializadas como JSON no
        campo `aditional_info`
        '''
        pass


class PDFDocument(Document):
    '''
    Um documento PDF
    '''
    document = models.OneToOneField(
        Document, on_delete=models.CASCADE, parent_link=True)
    pdf_file = models.FileField(
        verbose_name="Arquivo", upload_to=settings.PDF_ARTIFACT_DIR)

    class Meta:
        verbose_name = "Documento PDF"
        verbose_name_plural = "Documentos PDF"

    def save(self, *args, **kwargs):
        self.determine_mime_type()
        if not self.title:
            try:
                self.title = Path(self.pdf_file.name).name
            except:
                self.title = "Documento PDF {}".format(self.pk)
        super(PDFDocument, self).save(*args, **kwargs)

    def determine_mime_type(self):
        try:
            self.mime_type = magic.from_file(self.the_file.name, mime=True)
        except:
            self.mime_type = 'application/pdf'



class NewsPDFCapture(models.Model):
    '''
    Um documento PDF para uma captura de página de uma notícia
    '''
    news = models.ForeignKey(
        'News', on_delete=models.SET_NULL, null=True, related_name="pdf_captures")
    pdf_document = models.OneToOneField(PDFDocument, on_delete=models.CASCADE)
    pdf_capture_date = models.DateTimeField(auto_now_add=True, verbose_name='Data de captura', blank=True, null=True,
                                            help_text='Data desta captura')

    class Meta:
        verbose_name = "Captura de Notícia em PDF"
        verbose_name_plural = "Capturas de Notícia em PDF"


class News(Artifact):
    '''
    Uma notícia da Internet
    '''
    url = models.URLField(
        max_length=255, help_text="Endereço original da notícia",
        verbose_name="Endereço", unique=True)
    archived_news_url = models.URLField(
        max_length=255, help_text="Endereço da notícia no <a href='https://archive.org/'>Archive.org</a>",
        verbose_name="Endereço no Internet Archive", unique=True, null=True, blank=True)
    # TODO: fazer um relacionamento com um artefato do tipo imagem
    authors = models.TextField(
        blank=True, verbose_name="Autores", help_text='Nomes dos autores, separados por vírgula')
    image = models.ImageField(
        blank=True, verbose_name="Imagem principal")
    body = models.TextField(
        blank=True, verbose_name="Texto da notícia", help_text="Texto integral da notícia")
    published_date = models.DateTimeField(verbose_name='Data de publicação', blank=True, null=True,
                                          help_text='Data em que a notícia foi publicada')

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"

    def save(self, *args, **kwargs):
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

    @property
    def has_basic_info(self):
        '''
        Retorna verdadeiro se ao menos um dos campos básicos estiver preenchido
        TODO: acrescentar campos de relacionamento e não verificar eles se o objeto for novo.
        '''
        return (bool(self.title) or bool(self.teaser) or bool(self.body) or bool(self.authors) or
                bool(self.image) or bool(self.published_date))

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
        response = requests.get(
            "https://archive.org/wayback/available?url={}".format(self.url))
        response.raise_for_status()
        response = response.json()

        if (response["archived_snapshots"] and response["archived_snapshots"]["closest"] and
                response["archived_snapshots"]["closest"]["available"]):
            closest_archive = response["archived_snapshots"]["closest"]
            self.archived_news_url = closest_archive["url"]

    @staticmethod
    @lru_cache(maxsize=2)
    def fetch_basic_info(url):
        '''
        Dada uma URL, extraia informações básicas sobre uma notícia usando as bibliotecas newspaper3k e goose
        '''
        # Tente extrair primeiro usando o newspaper3k e reutilize seu html, se possível
        newspaper_article = News.extract_using_newspaper(url)
        if newspaper_article:
            goose_article = News.extract_using_goose3(
                url, newspaper_article.html)
        else:
            goose_article = News.extract_using_goose3(url)
        if newspaper_article is None and goose_article is None:
            raise(Exception(
                'Não foi possível extrair informações básicas sobre a notícia, pois nenhum dos extratores funcionou.'))
        basic_info = News.merge_extractions(
            newspaper_article, goose_article)
        return basic_info

    @log_process(operation="buscar informações básicas", object_type="Notícia")
    def set_basic_info(self):
        '''
        Abre a página da notícia e tenta inferir e definir suas informações básicas
        '''
        basic_info = News.fetch_basic_info(self.url)
        for prop, value in basic_info.items():
            if prop == 'keywords':
                setattr(self, '_keywords', value)
            else:
                setattr(self, prop, value)

    @staticmethod
    def extract_using_newspaper(url, raw_html=None):
        '''
        Tenta extrair usando a biblioteca newspaper3k
        '''
        try:
            newspaper_article = Article(url)

            if raw_html:
                newspaper_article.download(input_html=raw_html)
            else:
                newspaper_article.download()
            newspaper_article.parse()
            newspaper_article.nlp()

            return newspaper_article
        except:
            return None

    @staticmethod
    def extract_using_goose3(url, raw_html=None):
        '''
        Tenta extrair usando a biblioteca goose3
        '''
        try:
            goose = Goose({'enable_image_fetching': True})

            if raw_html:
                goose_article = goose.extract(raw_html=raw_html, url=url)
            else:
                goose_article = goose.extract(url=url)

            return goose_article
        except:
            return None

    @staticmethod
    def merge_extractions(newspaper_article, goose_article):
        '''
        Com base nas extrações passadas, constrói um dicionário em que a informação de cada uma é aproveitada, se existir.
        '''
        def join_with_comma(list):
            return ",".join(list)

        try:
            # TODO: melhorar esse código, que está safo, mas feio pra caramba
            news_dict = {
                'title': newspaper_article.title if getattr(newspaper_article, 'title', None) else getattr(goose_article, 'title', None),
                'image': newspaper_article.top_image if getattr(newspaper_article, 'top_image', None) else goose_article.top_image.src if isinstance(getattr(goose_article, 'top_image', None), Image) else None,
                'body': newspaper_article.text if getattr(newspaper_article, 'text', None) else getattr(goose_article, 'cleaned_text', None),
                'teaser': getattr(newspaper_article, 'summary', None),

                'published_date': newspaper_article.publish_date if getattr(newspaper_article, 'publish_date', None) else getattr(goose_article, 'publish_date', None),

                'authors': join_with_comma(newspaper_article.authors if getattr(newspaper_article, 'authors', []) else getattr(goose_article, 'authors', [])),
                'keywords': newspaper_article.keywords if getattr(newspaper_article, 'keywords', []) else getattr(goose_article, 'tags', []),
            }
            return news_dict
        except Exception as err:
            raise(
                Exception(
                    "Falha ao construir o dicionário com as informações básicas da notícia: {}."
                    .format(str(err))
                )
            )

    @job
    @log_process(operation="adicionar uma captura em formato PDF", object_type="Notícia")
    def add_pdf_capture(self):
        '''
        Captura a notícia em formato para impressão e em PDF
        '''

        # TODO: checar se o diretório existe, se existem permissões para salvar etc
        # TODO: usar o System check framework
        if not settings.PDF_ARTIFACT_DIR:
            raise ValueError(
                'O caminho para onde salvar as páginas não foi definido (constante de configuração PDF_ARTIFACT_DIR).')

        uniq_filename = (
            str(datetime.datetime.now().date()) + '_' +
            str(datetime.datetime.now().time()).replace(':', '.') + '.pdf'
        )

        pdf_path = settings.PDF_ARTIFACT_DIR + uniq_filename
        file_pdf_path = str(Path(settings.MEDIA_ROOT, pdf_path))

        pdfkit.from_url(self.url, file_pdf_path, options={
            'print-media-type': None,
            'disable-javascript': None,
        })

        pdf_document = PDFDocument.objects.create(
            pdf_file=pdf_path, is_user_object=False)

        news_pdf_capture = NewsPDFCapture.objects.create(
            news=self, pdf_document=pdf_document)

    def add_fetched_keywords(self):
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
