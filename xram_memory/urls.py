from .page.views import InMenuStaticPagesViewSet, StaticPageViewSet, FeaturedStaticPagesViewSet
from xram_memory.artifact.views import DocumentViewSet, NewsViewSet, AlbumViewSet
from xram_memory.taxonomy.views import SubjectViewSet
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
    # Páginas
    path('api/v1/pages/in_menu',
         InMenuStaticPagesViewSet.as_view({'get': 'listing'})),
    path('api/v1/pages/featured',
         FeaturedStaticPagesViewSet.as_view({'get': 'listing'})),
    path('api/v1/pages/<str:url>',
         StaticPageViewSet.as_view({'get': 'retrieve'})),
    # Documentos
    path('api/v1/document/<str:document_id>',
         DocumentViewSet.as_view({'get': 'retrieve'})),
    # Páginas de Documentos
    path('api/v1/document/<str:document_id>/pages',
         DocumentViewSet.as_view({'get': 'retrieve_pages'})),
    # Notícias
    path('api/v1/news/<str:slug>',
         NewsViewSet.as_view({'get': 'retrieve'})),
    # Álbuns
    path('api/v1/albums',
         AlbumViewSet.as_view({'get': 'listing'})),
    path('api/v1/album/<str:album_id>',
         AlbumViewSet.as_view({'get': 'retrieve'})),
    # Taxonomia
    path('api/v1/subjects/featured',
         SubjectViewSet.as_view({'get': 'featured'})),
    path('api/v1/subjects/initial/<str:initial>',
         SubjectViewSet.as_view({'get': 'subjects_by_initial'})),
    path('api/v1/subjects/initials',
         SubjectViewSet.as_view({'get': 'subjects_initials'})),
    path('api/v1/subject/<str:subject_slug>',
         SubjectViewSet.as_view({'get': 'retrieve'})),
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
