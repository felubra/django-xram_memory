from easy_thumbnails.widgets import ImageClearableFileInput
from easy_thumbnails.fields import ThumbnailerField
from tags_input import admin as tags_input_admin
from xram_memory.artifact.models import Document, DocumentPage
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

    def num_pages(self, object):
        return object.num_pages
    num_pages.short_description = "Número de páginas"


DocumentAdmin.readonly_fields = DocumentAdmin.readonly_fields + \
    ('mime_type', 'document_id', 'num_pages')
DocumentAdmin.fieldsets = FileAdmin.build_fieldsets(extra_main_fields=('document_id', 'keywords',
                                                                       'subjects', 'published_date',
                                                                       'num_pages',
                                                                       ),
                                                    extra_advanced_fields=(
                                                        "mime_type",)
                                                    )


@admin.register(DocumentPage)
class DocumentPageAdmin(DocumentAdmin):
    def has_view_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
