from django.contrib import admin
from models import *

class LayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'layerName', 'provider', 'public', 'minzoom', 'maxzoom')
    list_filter = ('public', 'provider')
    list_editable = ('public',)

admin.site.register(Layer, LayerAdmin)
