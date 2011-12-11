# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AppDocs'
        db.create_table('upload_appdocs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['application.Applicant'], unique=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('edu_certificate', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('abroad_edu_certificate', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('gat_score', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('pat1_score', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('pat3_score', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('anet_score', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('nat_id', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('app_fee_doc', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('last_uploaded_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('num_uploaded_today', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('upload', ['AppDocs'])


    def backwards(self, orm):
        
        # Deleting model 'AppDocs'
        db.delete_table('upload_appdocs')


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
        'upload.appdocs': {
            'Meta': {'object_name': 'AppDocs'},
            'abroad_edu_certificate': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'anet_score': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'app_fee_doc': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['application.Applicant']", 'unique': 'True'}),
            'edu_certificate': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'gat_score': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_uploaded_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'nat_id': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'num_uploaded_today': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pat1_score': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'pat3_score': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['upload']
