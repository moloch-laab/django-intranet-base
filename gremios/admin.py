from django.contrib import admin

from .models import RutGremio, Cartola

class RutGremioAdmin(admin.ModelAdmin):
    list_display = ('rut','active', 'timestamp', 'updated', 'user_id',)
    list_filter = ('rut','active', 'timestamp', 'updated', 'user_id',)
    ordering = ('rut', 'active', 'timestamp', 'updated', 'user_id',)

class CartolaAdmin(admin.ModelAdmin):
    list_display = ('rut_gremio_id', 'desde', 'hasta', 'pub_date', 'active', 'updated')
    list_filter = ('rut_gremio_id', 'desde', 'hasta', 'pub_date', 'active', 'updated')
    ordering = ('rut_gremio_id', 'desde', 'hasta', 'pub_date', 'active', 'updated')

admin.site.register(RutGremio, RutGremioAdmin)
admin.site.register(Cartola, CartolaAdmin)