from django.contrib import admin
from filer.admin.fileadmin import FileAdmin
from xram_memory.artifact.models import Document
from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerField


@admin.register(Document)
class DocumentAdmin(FileAdmin):
    list_display = (
        'id',
        'folder',
        'file',
        'name',
        'owner',
        'uploaded_at',
        'modified_at',
        'mime_type',
        'is_user_object',
    )
    list_filter = (
        'folder',
        'owner',
        'uploaded_at',
        'modified_at',
        'is_public',
        'is_user_object',
    )
    date_hierarchy = 'uploaded_at'
    search_fields = ('name',)
    formfield_overrides = {
        ThumbnailerField: {'widget': ImageClearableFileInput},
    }


DocumentAdmin.readonly_fields = DocumentAdmin.readonly_fields + ('mime_type',)
DocumentAdmin.fieldsets = FileAdmin.build_fieldsets(
    extra_advanced_fields=("mime_type",))
