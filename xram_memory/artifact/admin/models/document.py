from tags_input import admin as tags_input_admin
from xram_memory.artifact.models import Document
from filer.admin.fileadmin import FileAdmin
from django.contrib import admin


@admin.register(Document)
class DocumentAdmin(FileAdmin, tags_input_admin.TagsInputAdmin):
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


DocumentAdmin.readonly_fields = DocumentAdmin.readonly_fields + \
    ('mime_type', 'document_id',)
DocumentAdmin.fieldsets = FileAdmin.build_fieldsets(extra_main_fields=('document_id', 'keywords',
                                                                       'subjects', 'published_date',
                                                                       ),
                                                    extra_advanced_fields=(
                                                        "mime_type",)
                                                    )
