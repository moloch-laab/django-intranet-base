from django.contrib import admin

from .models import RutGremio, Cartola

class RutGremioAdmin(admin.ModelAdmin):
    list_display = ('rut',)
    list_filter = ('rut',)
    ordering = ('rut',)

class CartolaAdmin(admin.ModelAdmin):
    list_display = ('rut_gremio', 'desde', 'hasta', 'pub_date')
    list_filter = ('rut_gremio', 'desde', 'hasta', 'pub_date')
    ordering = ('rut_gremio', 'desde', 'hasta', 'pub_date')

admin.site.register(RutGremio, RutGremioAdmin)
admin.site.register(Cartola, CartolaAdmin)