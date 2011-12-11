# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Announcement'
        db.create_table('commons_announcement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('commons', ['Announcement'])

        # Adding model 'Log'
        db.create_table('commons_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('applicant_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('applicantion_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('commons', ['Log'])


    def backwards(self, orm):
        
        # Deleting model 'Announcement'
        db.delete_table('commons_announcement')

        # Deleting model 'Log'
        db.delete_table('commons_log')


    models = {
        'commons.announcement': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Announcement'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'commons.log': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Log'},
            'applicant_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'applicantion_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['commons']
