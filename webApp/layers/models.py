from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos.point import Point
from django.conf import settings

import jsonfield

import logging
import sqlite3

class Layer(models.Model):
    """
    Defines a TileStache layer
    """

    PROVIDER_CHOICES = (
        ('mapnik', 'Mapnik'),
        ('mbtiles', 'MBTiles'),
        ('url template', 'URL template'),
        ('vector', 'Vector'),
        ('other', 'Provider Class'),
    )

    FORMAT_CHOICES = (
        ('png', 'png'),
        ('jpg', 'jpg'),
        ('json', 'json'),
    )

    PROJECTION_CHOICES = (
        ('spherical mercator', 'spherical mercator'),
        ('WGS84', 'WGS84'),
    )

    DRIVER_CHOICES = (
        ('ESRI Shapefile', 'ESRI Shapefile'),
        ('PostgreSQL', 'PostgreSQL'),
        ('GeoJSON', 'GeoJSON'),
    )

    CLASS_CHOICES = (
        ('TileStache.Goodies.VecTiles:Provider', 'Tilestache VecTiles'),
    )

    #meta data fields
    attribution = models.CharField(max_length=255, blank=True, null=True)
    bounds = models.PolygonField(blank=True, null=True)
    center = models.PointField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    legend = models.TextField(max_length=5000, blank=True, null=True)
    maxzoom = models.IntegerField(blank=True, null=True)
    minzoom = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    public = models.BooleanField(default=True)
    version = models.CharField(default="1.0", max_length=20)
    
    #tileStache config
    layerName = models.CharField(max_length=50, unique=True)
    provider = models.CharField(max_length=100, choices=PROVIDER_CHOICES, 
        default='mbtiles')
    uploadedFile = models.FileField(blank=True, null=True, 
        upload_to=settings.UPLOAD_DIR)
    localFile = models.CharField(max_length=500, blank=True, null=True)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, 
        default="png")
    template = models.URLField(blank=True, max_length=1000, 
        verbose_name="URL for Template provider")
    projection = models.CharField(max_length=20, default='spherical mercator', 
        choices=PROJECTION_CHOICES)
    sourceProjection = models.CharField(max_length=20, blank=True, null=True, 
        choices=PROJECTION_CHOICES)
    metatileRows = models.IntegerField(default=1)
    metatileColumns = models.IntegerField(default=1)
    metatileBuffer = models.IntegerField(default=0)
    referer = models.URLField(blank=True, null=True, max_length=1000,
        verbose_name="Referer for Template provider queries")
    parameters = jsonfield.JSONField(blank=True, null=True, 
        verbose_name="Json parameters block for vector provider")
    driver = models.CharField(blank=True, null=True, max_length=30, 
        choices=DRIVER_CHOICES,
        verbose_name="Driver for vector provider")
    allowed_origin = models.CharField(max_length=200, default="*")
    provider_class = models.CharField(max_length=200, blank=True, null=True, 
        verbose_name="Class name for other Provider class",
        choices=CLASS_CHOICES)
    objects = models.GeoManager()

    def get_tile_url(self):
        return "%s/tiles/%s/{z}/{x}/{y}.%s" % (settings.BASE_URL, self.layerName, self.format)

    def get_tile_url_array(self):
        urls = []
        urls.append(self.get_tile_url())
        return urls

    def preview_zoom(self):
        return self.minzoom + ((self.maxzoom - self.minzoom) /2)

    def best_file(self):
        if self.localFile is not None and len(self.localFile) > 0:
            return self.localFile
        if self.uploadedFile is not None:
            try:
                return self.uploadedFile.path
            except:
                return None
        return None

    def load_metadata_from_mbtiles(self):
        try:
            path = self.best_file()
            logging.debug("getting metadata from " + path)
            con = sqlite3.connect(path)
        except Exception, e:
            logging.error("Could not connect to database" + str(e))
            return
        
        metadata = dict(con.execute('select name, value from metadata;').fetchall())
        if 'attribution' in metadata and (self.attribution is None or len(self.attribution) == 0):
            self.attribution = metadata['attribution']
        if 'name' in metadata and (self.name is None or len(self.name) == 0):
            self.name = metadata['name']
        if 'description' in metadata and (self.description is None or len(self.description) == 0):
            self.description = metadata['description']
        if 'legend' in metadata and (self.legend is None or len(self.legend) == 0):
            self.legend = metadata['legend']
            
        if 'bounds' in metadata:
            (left, bottom, right, top) = metadata['bounds'].split(',')
            self.bounds = Polygon.from_bbox((float(left), float(bottom), float(right), float(top)))

        if 'center' in metadata:
            coords = metadata['center'].split(',')
            if len(coords) >= 2:
                self.center = Point(float(coords[0]), float(coords[1]))
        elif self.center is None and self.bounds is not None:
            self.center = self.bounds.centroid

        self.format = metadata.get('format', self.format)
        self.version = metadata.get('version', self.version)
        if 'minzoom' in metadata and 'maxzoom' in metadata:
            self.minzoom = int(metadata['minzoom'])
            self.maxzoom = int(metadata['maxzoom'])
        else:
            (minzoom, maxzoom) = con.execute('select min(zoom_level), max(zoom_level) from tiles').fetchone()
            self.minzoom = int(minzoom)
            self.maxzoom = int(maxzoom)

        con.close()


    def preview_url(self, request):
        return request.build_absolute_uri("/preview/%s/" % self.layerName)


    def get_layer_config(self):
        providerDict = {}
        if self.provider == "other":
            providerDict['class'] = self.provider_class
            if self.parameters is not None:
                providerDict['kwargs'] = self.parameters
        else:
            providerDict['name'] = self.provider

        providerDict['projection'] = self.projection

        if self.provider == "mbtiles":
            providerDict['tileset'] = self.best_file()
        elif self.provider == "mapnik":
            providerDict['mapfile'] = self.best_file()
        elif self.provider == "url template":
            providerDict['template'] = self.template
            if self.referer is not None:
                providerDict['referer'] = self.referer
            if self.sourceProjection is not None:
                providerDict['source projection'] = self.sourceProjection            
        elif self.provider == "vector":
            if self.parameters is not None:
                providerDict['parameters'] = self.parameters
            if self.driver is not None:
                providerDict['driver'] = self.driver

        metatile = {"rows" : self.metatileRows,
         "columns" : self.metatileColumns,
         "buffer" : self.metatileBuffer }

        config = {'provider' : providerDict, 'metatile' : metatile}
        if self.allowed_origin is not None:
            config['allowed origin'] = self.allowed_origin
        
        return config


    def get_bounds_array(self):
        if self.bounds is not None:
            coords = self.bounds.boundary.coords
            return (coords[0][0], coords[0][1], coords[2][0], coords[2][1])
        return None

    def get_center_array(self):
        return (self.center.x, self.center.y)
