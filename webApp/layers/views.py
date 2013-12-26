from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.conf import settings

import logging

from layers.serializers import TileDirectorySerializer, TileJsonSerializer
from layers.models import *
import TileStache

class TileJson(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that provides a list of all available layers as tile json, and TileJson
    for each layer
    """
    queryset = Layer.objects.filter(public=True).all()
    serializer_class = TileJsonSerializer
    lookup_field = 'layerName'


class LayerAdmin(viewsets.ModelViewSet):
    """
    API endpoint for administration of layers.
    """
    queryset = Layer.objects.all()
    serializer_class = TileDirectorySerializer
    permission_classes = (IsAuthenticated,)


def tiles(request, layer_name, z, x, y, extension):
    """
    Fetch tiles with tilestache.
    """
    dbLayer = get_object_or_404(Layer, layerName=layer_name)
    metatile = TileStache.Core.Metatile()

    config = get_config()

    path_info = "%s/%s/%s/%s.%s" % (layer_name, z, x, y, extension)
    coord, extension = TileStache.splitPathInfo(path_info)[1:]
    tilestacheLayer = config.layers[layer_name]

    status_code, headers, content = tilestacheLayer.getTileResponse(coord, extension)
    mimetype = headers.get('Content-Type')
    if len(content) == 0:
        status_code = 404

    return HttpResponse(content, mimetype=mimetype, status=status_code)


def get_config():
    """
    Get TileStache confiuration.
    """
    config_dict = get_base_config_dict()
    for layer in Layer.objects.all():
        providerDict = {'name' : layer.provider}
        if layer.provider == "mbtiles":
            providerDict['tileset'] = layer.bestFile()
        elif layer.provider == "mapnik":
            providerDict['mapfile'] = layer.bestFile()
        config_dict['layers'][layer.layerName] = {'provider' : providerDict}

    return TileStache.Config.buildConfiguration(config_dict)


def get_base_config_dict():
    """
    Get the base tile stache configuration dictionary, layers get added to this to build a config.
    """
    config = {}
    config['cache'] = settings.TILESTACHE_CACHE
    config['layers'] = {}
    return config


class LayerPreviewView(TemplateView):
    """
    View that displays a map with leaflet to preview a map layer.
    """
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super(LayerPreviewView, self).get_context_data(**kwargs)
        context['layer'] = get_object_or_404(Layer, layerName=kwargs['layer_name'])
        return context


class UploadFileView(CreateView):
    """
    A form view with to upload a file and create a new layer.
    """
    model = Layer
    fields = ['name', 'attribution', 'description', 'layerName', 'provider', 'public',
         'localFile', 'uploadedFile']
    template_name = "layer_upload_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        obj = form.save(commit=False)
        obj.save()
        if obj.provider == "mbtiles":
            try:
                obj.loadMetaDataFromMBTiles()
                obj.save()
            except Exception, e:
                logging.error("Error getting metadata from upload " + str(e))
        return super(UploadFileView, self).form_valid(form)


class IndexView(TemplateView):
    template_name = "index.html"

