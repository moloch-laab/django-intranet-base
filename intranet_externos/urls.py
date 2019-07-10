from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from core.urls import core_patterns
from common.urls import common_patterns
from gremios.urls import gremios_patterns

urlpatterns = [
    path('', include(core_patterns)),
    path('gremios/', include(gremios_patterns)),
    path('admin/', admin.site.urls),
    # Paths del auth
    path('', include(common_patterns)),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)