from xram_memory.artifact.models import Artifact, Document, Newspaper
from django.db import models, transaction, IntegrityError
from xram_memory.taxonomy.models import Keyword, Subject
from xram_memory.logger.decorators import log_process
from easy_thumbnails.files import get_thumbnailer
from django.core.files import File as DjangoFile
from django.core.validators import URLValidator
from boltons.cacheutils import cachedproperty
from django.utils.encoding import iri_to_uri
from filer.fields.file import FilerFileField
from django.urls import get_script_prefix
from xram_memory.lib import NewsFetcher
from django.db.models import Prefetch
from django.utils.timezone import now
from filer.models import Folder
from django.conf import settings
from pathlib import Path
import datetime


class News(Artifact):
    """
    Uma notícia capturada da Internet

    Este modelo gerará um artefato do tipo notícia e possivelmente outros artefatos como uma captura
    de página (NewsPDFCapture) e uma imagem associada a notícia (NewsImageCapture).
    """

    url = models.URLField(
        verbose_name="Endereço original",
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
        help_text="Nomes dos autores, separados por vírgula",
        blank=True,
    )
    body = models.TextField(
        verbose_name="Texto da notícia",
        help_text="Texto integral da notícia",
        null=True,
        blank=True,
    )
    published_date = models.DateTimeField(
        verbose_name="Data de publicação",
        help_text="Data em que a notícia foi publicada",
        blank=True,
        null=True,
    )
    language = models.CharField(max_length=2, null=True, blank=True, default="pt")
    newspaper = models.ForeignKey(
        Newspaper, null=True, on_delete=models.SET_NULL, related_name="news"
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
            raise ValueError("Você precisa definir um endereço para a notícia.")

        if not self.title:
            self.set_web_title()

        # salva a notícia
        super().save(*args, **kwargs)

    @property
    def has_basic_info(self):
        """
        Indica se esta notícia tem ao menos alguns campos preenchidos, ou seja, informações básicas.
        """
        return (
            bool(self.title)
            or bool(self.teaser)
            or bool(self.body)
            or bool(self.authors)
            or bool(self.published_date)
        )

    @property
    def has_pdf_capture(self):
        """
        Indica se existe ao menos uma captura em pdf associada a esta notícia.
        """
        try:
            return (
                self.pdf_captures.prefetch_related(Prefetch("news")).all().count() > 0
            )
        except:
            return False

    @property
    def has_image(self):
        """
        Indica se esta notícia tem uma imagem associada.
        """
        try:
            image_capture = self.image_capture
            return image_capture is not None
        except:
            return False

    @log_process(operation="pegar o título")
    def set_web_title(self):
        """
        Pega o título para a página desta notícia.
        """
        title = NewsFetcher.fetch_web_title(self.url)[:255]
        if title:
            self.title = title

    @log_process(operation="verificar por uma versão no archive.org")
    def fetch_archived_url(self):
        """
        Verifica se existe e adiciona a URL de uma versão arquivada desta notícia presente no
        `Internet Archive`.
        """
        archived_news_url = NewsFetcher.fetch_archived_url(self.url)
        if archived_news_url:
            self.archived_news_url = archived_news_url

    @log_process(operation="buscar informações básicas")
    def set_basic_info(self):
        """
        Abre a página da notícia e tenta inferir e definir suas informações básicas.
        """
        basic_info = NewsFetcher.fetch_basic_info(self.url)
        # preenche os campos do modelo com as informações obtidas e lida com casos especiais
        for prop, value in basic_info.items():
            if prop in ("keywords", "subjects"):
                setattr(self, "_{}".format(prop), value)
            elif prop == "image":
                setattr(self, "_image", value)
            else:
                setattr(self, prop, value)
        return basic_info

    @log_process(operation="adicionar uma captura em formato PDF")
    def add_pdf_capture(self):
        """
        Captura a notícia em formato para impressão e em PDF.
        TODO: usar um hash com sal na geração do nome do arquivo.
        """
        import hashlib

        uniq_filename = (
            str(datetime.datetime.now().date())
            + "_"
            + str(datetime.datetime.now().time()).replace(":", ".")
        )
        filename = (
            hashlib.md5(
                "{}{}".format(uniq_filename, settings.FILE_HASHING_SALT).encode("utf-8")
            ).hexdigest()
            + ".pdf"
        )

        with NewsFetcher.get_pdf_capture(self.url) as fd:
            django_file = DjangoFile(fd, name=filename)
            with transaction.atomic():
                folder = Folder.objects.get(**settings.FOLDER_PDF_CAPTURES)
                new_pdf_document = Document(
                    file=django_file,
                    name=filename,
                    original_filename=filename,
                    folder=folder,
                    owner=self.modified_by,
                    published_date=now(),
                    is_user_object=False,
                    is_public=True,
                )
                # Reaproveite um arquivo já existente, com base no seu hash, de forma que um
                # arquivo possa ser utilizado várias vezes, por várias capturas. Ao que parece,
                # contudo o wkhtmltopdf sempre gera arquivos diferentes...
                try:
                    pdf_document = Document.objects.get(sha1=new_pdf_document.sha1)
                except Document.DoesNotExist:
                    new_pdf_document.save()
                    pdf_document = new_pdf_document

                NewsPDFCapture.objects.create(news=self, pdf_document=pdf_document)

    @log_process(operation="adicionar palavras-chave")
    def add_fetched_keywords(self):
        """
        Para cada uma das palavras-chave descobertas por set_basic_info(), crie uma palavra-chave no
        banco de dados e associe ela a esta notícia
        """
        if hasattr(self, "_keywords") and len(self._keywords) > 0:
            keywords = []
            for keyword in self._keywords:
                try:
                    # tente achar a palavra-chave pelo nome
                    keywords.append(Keyword.objects.get(name=keyword))
                except Keyword.DoesNotExist:
                    try:
                        keywords.append(
                            Keyword.objects.create(
                                name=keyword,
                                created_by=self.modified_by,
                                modified_by=self.modified_by,
                            )
                        )
                    except IntegrityError:
                        pass
            if len(keywords):
                self.keywords.add(*keywords)

    @log_process(operation="adicionar assuntos")
    def add_fetched_subjects(self):
        """
        Para cada uma dos assuntos descobertos por set_basic_info(), crie um assunto no banco de
        dados e associe ele a esta notícia
        """
        if hasattr(self, "_subjects") and len(self._subjects) > 0:
            subjects = []
            for subject in self._subjects:
                try:
                    # tente achar a assunto pelo nome
                    subjects.append(Subject.objects.get(name=subject))
                except Subject.DoesNotExist:
                    try:
                        subjects.append(
                            Subject.objects.create(
                                name=subject,
                                created_by=self.modified_by,
                                modified_by=self.modified_by,
                            )
                        )
                    except IntegrityError:
                        pass
            if len(subjects):
                self.subjects.add(*subjects)

    @log_process(operation="baixar uma imagem")
    def add_fetched_image(self):
        """
        Com base na url da imagem descoberta por set_basic_info(), baixa a imagem e cria uma
        instância dela como documento de artefato (Document) e captura de imagem de notícia
        (NewsImageCapture).
        TODO: usar um hash com sal na geração do nome do arquivo.
        """
        original_filename = Path(self._image).name
        original_extension = Path(self._image).suffix
        import hashlib

        filename = (
            hashlib.md5(
                "{}{}".format(self._image, settings.FILE_HASHING_SALT).encode("utf-8")
            ).hexdigest()
            + original_extension[:4]
        )

        with NewsFetcher.fetch_image(self._image) as fd:
            django_file = DjangoFile(fd, name=filename)
            with transaction.atomic():
                # tente apagar todas as imagens associadas a esta notícia, pois só pode haver uma
                try:
                    captures_for_this_news = self.image_capture
                    captures_for_this_news.delete()
                except (NewsImageCapture.DoesNotExist):
                    pass  # Não existem imagens associadas a esta notícia
                folder = Folder.objects.get(**settings.FOLDER_IMAGE_CAPTURES)

                new_image_document = Document(
                    file=django_file,
                    name=filename,
                    original_filename=original_filename,
                    is_user_object=False,
                    folder=folder,
                    published_date=now(),
                    owner=self.modified_by,
                    is_public=True,
                )
                # Reaproveite um arquivo já existente, com base no seu hash,
                # de forma que um arquivo possa ser utilizado várias vezes, por várias capturas.
                try:
                    image_document = Document.objects.get(sha1=new_image_document.sha1)
                except Document.DoesNotExist:
                    new_image_document.save()
                    image_document = new_image_document

                _ = (
                    image_document.thumbnail
                )  # força a geração de um thumbnail para esta captura

                NewsImageCapture.objects.create(
                    image_document=image_document, original_url=self._image, news=self
                )

        # limpe o cache das flags/campos que dependem de uma captura de imagem
        for attr_name in ["thumbnails"]:
            try:
                delattr(self, attr_name)
            except AttributeError:
                pass

    @property
    def image_capture_indexing(self):
        """
        Retorna a url para uma captura de imagem desta notícia, se existente.
        """
        return self.thumbnails.get("image_capture", None)

    @property
    def thumbnail(self):
        """
        Retorna a url para uma miniatura de uma captura de página desta notícia, se existente.
        """
        return self.thumbnails.get("thumbnail", None)

    @cachedproperty
    def thumbnails(self):
        """
        Retorna uma lista de thumbnails geradas
        """
        thumbnails_aliases = settings.THUMBNAIL_ALIASES[""].keys()
        generated_thumbnails = {}
        try:
            if self.image_capture:
                for alias in thumbnails_aliases:
                    try:
                        generated_thumbnails[alias] = get_thumbnailer(
                            self.image_capture.image_document.file
                        )[alias].url
                    except:
                        continue
        except:
            return {}
        else:
            return generated_thumbnails

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

    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix() + "news/{}".format(self.slug))


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
    pdf_document = FilerFileField(
        verbose_name="Documento PDF",
        on_delete=models.CASCADE,
        related_name="pdf_capture",
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
            return 'Captura em PDF de "{}"'.format(self.news.url)
        except AttributeError:
            return "Captura em PDF de notícia"

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.pdf_document.delete()


class NewsImageCapture(models.Model):
    """
    Um documento PDF para uma captura de página de uma notícia
    """

    news = models.OneToOneField(
        News,
        verbose_name="Notícia",
        on_delete=models.CASCADE,
        null=True,
        related_name="image_capture",
    )
    image_document = FilerFileField(
        verbose_name="Documento de imagem",
        on_delete=models.CASCADE,
        related_name="image_capture",
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
            return 'Imagem principal de "{}"'.format(self.news.url)
        except AttributeError:
            return "Imagem principal de notícia"

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.image_document.delete()
