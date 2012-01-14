# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AdditionalEducation'
        db.create_table('quota_additionaleducation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Applicant'])),
            ('training_round', self.gf('django.db.models.fields.IntegerField')()),
            ('training_subject', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gpax', self.gf('django.db.models.fields.FloatField')()),
            ('pat3', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal('quota', ['AdditionalEducation'])


    def backwards(self, orm):
        
        # Deleting model 'AdditionalEducation'
        db.delete_table('quota_additionaleducation')


    models = {
        'application.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'activation_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'has_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_related_model': ('application.fields.IntegerListField', [], {'default': 'None'}),
            'hashed_password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'national_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'quota.additionaleducation': {
            'Meta': {'object_name': 'AdditionalEducation'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Applicant']"}),
            'gpax': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pat3': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'training_round': ('django.db.models.fields.IntegerField', [], {}),
            'training_subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['quota']
