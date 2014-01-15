from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos.point import Point
from django.conf import settings

import logging
import sqlite3

class Layer(models.Model):
    """
    Defines a TileStache layer
    """

    PROVIDER_CHOICES = (
        ('mapnik', 'mapnik'),
        ('mbtiles', 'MBTiles'),
    )

    FORMAT_CHOICES = (
        ('png', 'png'),
        ('jpg', 'jpg'),
        ('json', 'json'),
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
    provider = models.CharField(max_length=100, choices=PROVIDER_CHOICES, default='mbtiles')
    uploadedFile = models.FileField(blank=True, null=True, upload_to=settings.UPLOAD_DIR)
    localFile = models.CharField(max_length=500, blank=True, null=True)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default="png")

    objects = models.GeoManager()

    def getTileUrl(self):
        return "%s/tiles/%s/{z}/{x}/{y}.%s" % (settings.BASE_URL, self.layerName, self.format)

    def getTileUrlArray(self):
        urls = []
        urls.append(self.getTileUrl())
        return urls

    def previewZoom(self):
        return self.minzoom + ((self.maxzoom - self.minzoom) /2)

    def bestFile(self):
        if self.localFile is not None and len(self.localFile) > 0:
            return self.localFile
        return self.uploadedFile.path

    def loadMetaDataFromMBTiles(self):
        try:
            path = self.bestFile()
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
        (minzoom, maxzoom) = con.execute('select min(zoom_level), max(zoom_level) from tiles').fetchone()
        self.minzoom = int(minzoom)
        self.maxzoom = int(maxzoom)

        con.close()

    def previewUrl(self, request):
        return request.build_absolute_uri("/preview/%s/" % self.layerName)
    