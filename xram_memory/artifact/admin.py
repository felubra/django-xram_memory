from django.contrib import admin

from .models import Artifact


@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'polymorphic_ctype',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
    )
    list_filter = (
        'polymorphic_ctype',
        'created_by',
        'modified_by',
        'created_at',
        'modified_at',
    )
    date_hierarchy = 'created_at'
