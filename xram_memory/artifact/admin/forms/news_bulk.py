from django import forms
from loguru import logger


from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from xram_memory.artifact.tasks import add_news_task
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.admin.sites import site as default_site, AdminSite
from django.core.validators import URLValidator
from django.db.utils import IntegrityError

from xram_memory.admin import DefaultAdminSite


# Create your views here.

class URLForm(forms.Form):
    fieldsets = ()
    urls = forms.fields.CharField(widget=forms.widgets.Textarea, label="Endereços",
                                  help_text="Insira os endereços das notícias, um por linha")

    def clean_urls(self, *args, **kwargs):
        urls = self.cleaned_data['urls']
        if not urls:
            raise ValidationError("É necessário informar uma URL.")
        # 1) separe por linha, construa uma array com os valores
        urls = urls.split()

        url_validator = URLValidator()

        def is_valid(value):
            try:
                url_validator(value)
                return True
            except ValidationError:
                return False

        # 3) Filtre a array para somente urls válidas
        urls = [url for url in urls if is_valid(url)]
        # 4) Se não houver urls válidas, crie um erro de validação
        if not len(urls):
            raise ValidationError('Todos endereços informados são inválidos.',
                                  code='invalid',
                                  params={'urls': urls},
                                  )
        return urls


@staff_member_required
def news_bulk_insertion(request):
    admin_site = default_site
    if request.method == 'POST':
        # crie um formulário preenchido com os dados enviados
        form = URLForm(request.POST)
        if form.is_valid():
            # pegue as urls sanitizadas
            urls, = form.cleaned_data.values()
            # agende a execução de 5 tarefas por vez para criar notícias com base urls
            urls_and_user_id = ((url, request.user.id) for url in urls)
            add_news_task.throws = (IntegrityError,)
            add_news_task.chunks(urls_and_user_id, 5).group().apply_async()
            logger.info(
                'O usuário {username} solicitou a inserção de {n} notícia(s) de uma só vez pela interface administrativa.'.format(
                    username=request.user.username, n=len(urls)
                )
            )
            # dê um aviso das urls inseridas
            messages.add_message(request, messages.INFO,
                                 '{} endereço(s) de notícia adicionado(s) à fila para criação.'.format(len(urls)))
            # redirecione para a página inicial
            return HttpResponseRedirect(reverse("admin:artifact_news_changelist"))
        else:
            # renderize novamente o formulário para dar oportunidade do usuário corrigir os erros
            return render(request, 'news_bulk_insertion.html', {
                'form': form,
                'site_header': admin_site.site_header,
                'site_title': admin_site.site_title,
                'title': 'Inserir notícias',
            })
    else:
        # crie um formulário vazio
        form = URLForm()

    return render(request, 'news_bulk_insertion.html', {
        'form': form,
        'site_header': admin_site.site_header,
        'site_title': admin_site.site_title,
        'title': 'Inserir notícias',
    })
