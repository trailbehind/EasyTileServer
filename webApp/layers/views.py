from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView
from django.conf import settings

import logging

from layers.serializers import LayerAdminSerializer, TileJsonSerializer
from layers.models import *
from layers.config import get_config

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
    serializer_class = LayerAdminSerializer
    permission_classes = (IsAuthenticated,)


def tiles(request, layer_name, z, x, y, extension):
    """
    Fetch tiles with tilestache.
    """
    metatile = TileStache.Core.Metatile()

    config = get_config()

    path_info = "%s/%s/%s/%s.%s" % (layer_name, z, x, y, extension)
    coord, extension = TileStache.splitPathInfo(path_info)[1:]
    try:
        tilestacheLayer = config.layers[layer_name]
    except:
        return HttpResponseNotFound()
        
    status_code, headers, content = tilestacheLayer.getTileResponse(coord, extension)
    mimetype = headers.get('Content-Type')
    if len(content) == 0:
        status_code = 404

    response = HttpResponse(content, mimetype=mimetype, status=status_code)
    response['Access-Control-Allow-Origin'] = '*'
    return response

class LayerPreviewView(TemplateView):
    """
    View that displays a map with leaflet to preview a map layer.
    """
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super(LayerPreviewView, self).get_context_data(**kwargs)
        context['layer'] = get_object_or_404(Layer, layerName=kwargs['layer_name'])
        return context


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['layers'] = Layer.objects.filter(public=True)
        return context
