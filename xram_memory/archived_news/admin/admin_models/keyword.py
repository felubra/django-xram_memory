from xram_memory.archived_news.models import Keyword
from django.contrib import admin


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
