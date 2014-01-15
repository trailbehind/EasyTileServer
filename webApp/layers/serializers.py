from rest_framework import serializers
from layers.models import Layer

class TileDirectorySerializer(serializers.HyperlinkedModelSerializer):
    previewUrl = serializers.SerializerMethodField('get_preview_url')

    class Meta:
        model = Layer
        read_only = ('previewUrl',)

    def get_preview_url(self, obj):
        return obj.previewUrl(self.context['request'])


class TileJsonSerializer(serializers.ModelSerializer):
    tiles = serializers.Field(source="getTileUrlArray")
    uniqueTileCacheKey = serializers.Field(source="layerName")

    class Meta:
        model = Layer
        fields = ('attribution', 'bounds', 'center', 'description', 'legend', 'maxzoom', 
            'minzoom', 'name', 'version', 'uniqueTileCacheKey', 'tiles', )
