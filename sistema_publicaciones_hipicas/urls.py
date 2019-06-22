from django.contrib import admin
from django.urls import include, path
from gremios.urls import gremios_patterns
from accounts.urls import accounts_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('core.urls')),
    path('gremios/', include(gremios_patterns)),
    path('admin/', admin.site.urls),
    # Paths del auth
    path('', include(accounts_patterns)),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)