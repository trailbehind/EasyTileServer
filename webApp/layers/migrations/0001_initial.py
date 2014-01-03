# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Layer'
        db.create_table(u'layers_layer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribution', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('bounds', self.gf('django.contrib.gis.db.models.fields.PolygonField')(null=True, blank=True)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('legend', self.gf('django.db.models.fields.TextField')(max_length=5000, null=True, blank=True)),
            ('maxzoom', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('minzoom', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('version', self.gf('django.db.models.fields.TextField')(default='1.0')),
            ('layerName', self.gf('django.db.models.fields.TextField')(unique=True, max_length=50)),
            ('provider', self.gf('django.db.models.fields.TextField')(default='mbtiles', max_length=100)),
            ('uploadedFile', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('localFile', self.gf('django.db.models.fields.TextField')(max_length=500, null=True, blank=True)),
            ('format', self.gf('django.db.models.fields.TextField')(default='png', max_length=20)),
        ))
        db.send_create_signal(u'layers', ['Layer'])


    def backwards(self, orm):
        # Deleting model 'Layer'
        db.delete_table(u'layers_layer')


    models = {
        u'layers.layer': {
            'Meta': {'object_name': 'Layer'},
            'attribution': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bounds': ('django.contrib.gis.db.models.fields.PolygonField', [], {'null': 'True', 'blank': 'True'}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.TextField', [], {'default': "'png'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layerName': ('django.db.models.fields.TextField', [], {'unique': 'True', 'max_length': '50'}),
            'legend': ('django.db.models.fields.TextField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'localFile': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'maxzoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'minzoom': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.TextField', [], {'default': "'mbtiles'", 'max_length': '100'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uploadedFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.TextField', [], {'default': "'1.0'"})
        }
    }

    complete_apps = ['layers']