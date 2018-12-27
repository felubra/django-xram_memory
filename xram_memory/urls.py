from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import xram_memory.news_fetcher.views as newsfetcher_views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('admin/news_fetcher/basic_info', newsfetcher_views.return_basic_info),
]

urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
