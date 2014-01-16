# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Layer.template'
        db.add_column(u'layers_layer', 'template',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Layer.projection'
        db.add_column(u'layers_layer', 'projection',
                      self.gf('django.db.models.fields.CharField')(default='spherical mercator', max_length=20),
                      keep_default=False)

        # Adding field 'Layer.metatileRows'
        db.add_column(u'layers_layer', 'metatileRows',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Layer.metatileColumns'
        db.add_column(u'layers_layer', 'metatileColumns',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Layer.metatileBuffer'
        db.add_column(u'layers_layer', 'metatileBuffer',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Layer.template'
        db.delete_column(u'layers_layer', 'template')

        # Deleting field 'Layer.projection'
        db.delete_column(u'layers_layer', 'projection')

        # Deleting field 'Layer.metatileRows'
        db.delete_column(u'layers_layer', 'metatileRows')

        # Deleting field 'Layer.metatileColumns'
        db.delete_column(u'layers_layer', 'metatileColumns')

        # Deleting field 'Layer.metatileBuffer'
        db.delete_column(u'layers_layer', 'metatileBuffer')


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
            'metatileBuffer': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'metatileColumns': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'metatileRows': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'minzoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'projection': ('django.db.models.fields.CharField', [], {'default': "'spherical mercator'", 'max_length': '20'}),
            'provider': ('django.db.models.fields.CharField', [], {'default': "'mbtiles'", 'max_length': '100'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'template': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'uploadedFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '20'})
        }
    }

    complete_apps = ['layers']