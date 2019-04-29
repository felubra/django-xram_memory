from rest_framework.serializers import ModelSerializer, CharField

from .models import StaticPage


class StaticPageSerializer(ModelSerializer):
    """Um serializer com com todos os principais campos da página."""
    class Meta:
        model = StaticPage
        fields = ('title', 'teaser', 'url',
                  'body', 'image',
                  'show_in_menu', 'published', 'featured', 'created_at', 'modified_at')


class SimpleStaticPageSerializer(ModelSerializer):
    """Um serializer com apenas alguns campos para salvar espaço."""
    class Meta:
        model = StaticPage
        fields = ('title', 'teaser', 'url',
                  'show_in_menu', 'published', 'featured',)
