# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'AdditionalEducation.applicant'
        db.alter_column('quota_additionaleducation', 'applicant_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['application.Applicant'], unique=True))

        # Adding unique constraint on 'AdditionalEducation', fields ['applicant']
        db.create_unique('quota_additionaleducation', ['applicant_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'AdditionalEducation', fields ['applicant']
        db.delete_unique('quota_additionaleducation', ['applicant_id'])

        # Changing field 'AdditionalEducation.applicant'
        db.alter_column('quota_additionaleducation', 'applicant_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Applicant']))


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
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['application.Applicant']", 'unique': 'True'}),
            'gpax': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pat3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'training_round': ('django.db.models.fields.IntegerField', [], {}),
            'training_subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['quota']
