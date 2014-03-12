from layers.models import *
import TileStache

import logging
import json


def get_config():
    """
    Get TileStache confiuration.
    """
    config_dict = get_base_config_dict()
    for layer in Layer.objects.all():
        providerDict = {'name' : layer.provider}
        providerDict['projection'] = layer.projection

        if layer.provider == "mbtiles":
            providerDict['tileset'] = layer.best_file()
        elif layer.provider == "mapnik":
            providerDict['mapfile'] = layer.best_file()
        elif layer.provider == "url template":
            providerDict['template'] = layer.template
            if layer.referer is not None:
                providerDict['referer'] = layer.referer
            if layer.sourceProjection is not None:
                providerDict['source projection'] = layer.sourceProjection

        if layer.parameters is not None:
            providerDict['parameters'] = layer.parameters
        if layer.driver is not None:
            providerDict['driver'] = layer.driver

        metatile = {"rows" : layer.metatileRows,
         "columns" : layer.metatileColumns,
         "buffer" : layer.metatileBuffer }
        config_dict['layers'][layer.layerName] = {'provider' : providerDict, 'metatile' : metatile}
        config_dict['allowed origin'] = layer.allowed_origin
    #logging.debug(json.dumps(config_dict))

    return TileStache.Config.buildConfiguration(config_dict)


def get_base_config_dict():
    """
    Get the base tile stache configuration dictionary, layers get added to this to build a config.
    """
    config = {}
    config['cache'] = settings.TILESTACHE_CACHE
    config['layers'] = {}
    return config
