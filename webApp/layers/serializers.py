from rest_framework import serializers
from layers.models import Layer

class TileDirectorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Layer

class TileJsonSerializer(serializers.ModelSerializer):
    tiles = serializers.Field(source="getTileUrlArray")
    uniqueTileCacheKey = serializers.Field(source="layerName")

    class Meta:
        model = Layer
        fields = ('attribution', 'bounds', 'center', 'description', 'legend', 'maxzoom', 
            'minzoom', 'name', 'version', 'uniqueTileCacheKey', 'tiles', )
