from .page.views import StaticPagesViewSet
from xram_memory.artifact.views import DocumentViewSet, NewsViewSet, AlbumViewSet
from xram_memory.taxonomy.views import SubjectViewSet, KeywordViewSet
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

API_BASE = 'api/v1'
urlpatterns = [
    # Páginas
    path(API_BASE + '/pages',
         StaticPagesViewSet.as_view({'get': 'listing'})),
    path(API_BASE + '/page/<str:url>',
         StaticPagesViewSet.as_view({'get': 'retrieve'})),

    # Documentos
    path(API_BASE + '/document/<str:document_id>',
         DocumentViewSet.as_view({'get': 'retrieve'})),

    # Notícias
    path(API_BASE + '/news/<str:slug>',
         NewsViewSet.as_view({'get': 'retrieve'})),

    # Álbuns
    path(API_BASE + '/albums',
         AlbumViewSet.as_view({'get': 'listing'})),
    path(API_BASE + '/album/<str:album_id>',
         AlbumViewSet.as_view({'get': 'retrieve'})),

    # Taxonomia
    path(API_BASE + '/subjects',
         SubjectViewSet.as_view({'get': 'listing'})),
    path(API_BASE + '/subjects/initials',
         SubjectViewSet.as_view({'get': 'subjects_initials'})),
    path(API_BASE + '/subject/<str:subject_slug>',
         SubjectViewSet.as_view({'get': 'retrieve'})),
    path(API_BASE + '/subject/<str:subject_slug>/items',
         SubjectViewSet.as_view({'get': 'artifacts_for_subject'})),

    path(API_BASE + '/keywords',
         KeywordViewSet.as_view({'get': 'listing'})),
    path(API_BASE + '/keyword/<str:keyword_slug>/items',
         KeywordViewSet.as_view({'get': 'artifacts_for_keyword'})),
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
