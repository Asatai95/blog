from django.conf.urls import url
from django.contrib.auth import views, urls
from django.urls import  path, include
import sys
import os
sys.path.append(os.getcwd())

import mysite.views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('mysite.urls')),
    path('', include('mysite.urls', namespace="apps")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
