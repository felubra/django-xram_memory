from .page.views import InMenuStaticPagesViewSet, StaticPageViewSet, FeaturedStaticPagesViewSet
from xram_memory.artifact.views import DocumentViewSet, NewsViewSet, AlbumViewSet
from django.conf.urls.static import static
from django.urls import include, path
from django.conf import settings
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
]

# TODO: proteger, somente usuários autenticados
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Endpoints da API
urlpatterns = [
    path('api/v1/pages/<int:pk>',
         StaticPageViewSet.as_view({'get': 'retrieve'})),
    path('api/v1/pages/in_menu',
         InMenuStaticPagesViewSet.as_view({'get': 'listing'})),
    path('api/v1/pages/featured',
         FeaturedStaticPagesViewSet.as_view({'get': 'listing'})),
    path('api/v1/document/<int:pk>',
         DocumentViewSet.as_view({'get': 'retrieve'})),
    path('api/v1/news/<int:pk>',
         NewsViewSet.as_view({'get': 'retrieve'})),
    path('api/v1/albums',
         AlbumViewSet.as_view({'get': 'listing'})),
    path('api/v1/album/<int:pk>',
         AlbumViewSet.as_view({'get': 'retrieve'})),
] + urlpatterns

# URLs canônicas para documentos do Filer
urlpatterns = [
    path('filer/', include('filer.urls')),
] + urlpatterns


urlpatterns = [path('tags_input/', include('tags_input.urls',
                                           namespace='tags_input'))] + urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
