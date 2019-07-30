from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from django_intranet_base.apps.core.urls import core_patterns
from django_intranet_base.apps.common.urls import common_patterns

urlpatterns = [
    path('', include(core_patterns)),
    path('', include(common_patterns)), # custom auth
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')), # django auth
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)