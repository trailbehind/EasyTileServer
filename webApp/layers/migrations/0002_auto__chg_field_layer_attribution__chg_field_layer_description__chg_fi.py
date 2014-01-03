# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Layer.attribution'
        db.alter_column(u'layers_layer', 'attribution', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Layer.description'
        db.alter_column(u'layers_layer', 'description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Layer.format'
        db.alter_column(u'layers_layer', 'format', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Layer.version'
        db.alter_column(u'layers_layer', 'version', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Layer.provider'
        db.alter_column(u'layers_layer', 'provider', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Layer.layerName'
        db.alter_column(u'layers_layer', 'layerName', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50))

        # Changing field 'Layer.localFile'
        db.alter_column(u'layers_layer', 'localFile', self.gf('django.db.models.fields.CharField')(max_length=500, null=True))

        # Changing field 'Layer.name'
        db.alter_column(u'layers_layer', 'name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'Layer.attribution'
        db.alter_column(u'layers_layer', 'attribution', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Layer.description'
        db.alter_column(u'layers_layer', 'description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Layer.format'
        db.alter_column(u'layers_layer', 'format', self.gf('django.db.models.fields.TextField')(max_length=20))

        # Changing field 'Layer.version'
        db.alter_column(u'layers_layer', 'version', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Layer.provider'
        db.alter_column(u'layers_layer', 'provider', self.gf('django.db.models.fields.TextField')(max_length=100))

        # Changing field 'Layer.layerName'
        db.alter_column(u'layers_layer', 'layerName', self.gf('django.db.models.fields.TextField')(max_length=50, unique=True))

        # Changing field 'Layer.localFile'
        db.alter_column(u'layers_layer', 'localFile', self.gf('django.db.models.fields.TextField')(max_length=500, null=True))

        # Changing field 'Layer.name'
        db.alter_column(u'layers_layer', 'name', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

    models = {
        u'layers.layer': {
            'Meta': {'object_name': 'Layer'},
            'attribution': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bounds': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'default': "'png'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layerName': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'legend': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'localFile': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'maxzoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'minzoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'default': "'mbtiles'", 'max_length': '100'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uploadedFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '20'})
        }
    }

    complete_apps = ['layers']