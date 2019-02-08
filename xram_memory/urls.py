from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from xram_memory.artifact.admin.forms.news_bulk import news_bulk_insertion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/artifact/news/insert_bulk', news_bulk_insertion),
]

# TODO: proteger, somente usuários autenticados
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
