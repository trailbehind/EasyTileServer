from rest_framework import serializers
from layers.models import Layer
from layers import tasks

import logging


class LayerAdminSerializer(serializers.HyperlinkedModelSerializer):
    previewUrl = serializers.SerializerMethodField('get_preview_url')

    class Meta:
        model = Layer
        read_only = ('previewUrl',)

    def get_preview_url(self, obj):
        return obj.preview_url(self.context['request'])

    def restore_object(self, attrs, instance=None):
        instance = super(LayerAdminSerializer, self).restore_object(attrs, instance=instance)
        instance.save()
        if instance.provider == "mbtiles":
            try:
                instance.load_metadata_from_mbtiles()
                instance.save()
            except Exception, e:
                logging.error("Error getting metadata from upload " + str(e))
        #regenerate config
        #get_config(force=True)
        tasks.generate_config.delay()
        return instance


class TileJsonSerializer(serializers.ModelSerializer):
    tiles = serializers.Field(source="get_tile_url_array")
    uniqueTileCacheKey = serializers.Field(source="layerName")
    bounds = serializers.Field(source="get_bounds_array")
    center = serializers.Field(source="get_center_array")

    class Meta:
        model = Layer
        fields = ('attribution', 'bounds', 'center', 'description', 'legend', 'maxzoom', 
            'minzoom', 'name', 'version', 'uniqueTileCacheKey', 'tiles', )
