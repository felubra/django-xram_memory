from xram_memory.archived_news.models import Keyword
from django.contrib import admin

from xram_memory.base_models import TraceableAdminModel


@admin.register(Keyword)
class KeywordAdmin(TraceableAdminModel):
    list_display = ('id', 'name')
    search_fields = ('name',)
