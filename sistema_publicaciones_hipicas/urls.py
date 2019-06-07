from django.contrib import admin
from django.urls import include, path
from cartolas_gremios.urls import cartolas_gremios_patterns
from accounts.urls import accounts_patterns

urlpatterns = [
    path('', include('core.urls')),
    path('cartolas_gremios/', include(cartolas_gremios_patterns)),
    path('admin/', admin.site.urls),
    # Paths del auth
    path('', include(accounts_patterns)),
]