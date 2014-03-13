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
        config_dict['layers'][layer.layerName] = layer.get_layer_config()
    logging.debug(json.dumps(config_dict, indent=4, separators=(',', ': ')))
    
    return TileStache.Config.buildConfiguration(config_dict)


def get_base_config_dict():
    """
    Get the base tile stache configuration dictionary, layers get added to this to build a config.
    """
    config = {}
    config['cache'] = settings.TILESTACHE_CACHE
    config['layers'] = {}
    return config
