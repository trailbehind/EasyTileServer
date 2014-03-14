from layers.models import *
import TileStache
from django.core.cache import cache

import logging
import json
from django.conf import settings

CACHE_KEY = "config.json"

def get_config(force=False):
    """
    Get TileStache confiuration.
    """

    cached = cache.get(CACHE_KEY, None)
    if not force and cached is not None:
        return TileStache.Config.buildConfiguration(json.loads(cached))

    logging.debug("generating config")
    config_dict = get_base_config_dict()
    for layer in Layer.objects.all():
        config_dict['layers'][layer.layerName] = layer.get_layer_config()
    #logging.debug(json.dumps(config_dict, indent=4, separators=(',', ': ')))

    cache.set(CACHE_KEY, json.dumps(config_dict), 60*5)
    if settings.TILESTACHE_CONFIG_PATH is not None:
        with open(settings.TILESTACHE_CONFIG_PATH, 'w') as f:
            f.write(json.dumps(config_dict, indent=4, separators=(',', ': ')))

    return TileStache.Config.buildConfiguration(config_dict)


def get_base_config_dict():
    """
    Get the base tile stache configuration dictionary, layers get added to this to build a config.
    """
    config = {}
    config['cache'] = settings.TILESTACHE_CACHE
    config['layers'] = {}
    return config
