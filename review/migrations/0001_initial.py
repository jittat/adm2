# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ReviewField'
        db.create_table('review_reviewfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('applicant_note_help_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('admin_note_help_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('applicant_note_format', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('admin_note_format', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('review', ['ReviewField'])

        # Adding model 'ReviewFieldResult'
        db.create_table('review_reviewfieldresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Applicant'])),
            ('review_field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['review.ReviewField'])),
            ('is_passed', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('applicant_note', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('internal_note', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('review', ['ReviewFieldResult'])

        # Adding model 'CompletedReviewField'
        db.create_table('review_completedreviewfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('national_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('review_field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['review.ReviewField'])),
        ))
        db.send_create_signal('review', ['CompletedReviewField'])


    def backwards(self, orm):
        
        # Deleting model 'ReviewField'
        db.delete_table('review_reviewfield')

        # Deleting model 'ReviewFieldResult'
        db.delete_table('review_reviewfieldresult')

        # Deleting model 'CompletedReviewField'
        db.delete_table('review_completedreviewfield')


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
        'review.completedreviewfield': {
            'Meta': {'object_name': 'CompletedReviewField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'national_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'review_field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['review.ReviewField']"})
        },
        'review.reviewfield': {
            'Meta': {'ordering': "['order']", 'object_name': 'ReviewField'},
            'admin_note_format': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'admin_note_help_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'applicant_note_format': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'applicant_note_help_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'review.reviewfieldresult': {
            'Meta': {'object_name': 'ReviewFieldResult'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Applicant']"}),
            'applicant_note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_note': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'is_passed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'review_field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['review.ReviewField']"})
        }
    }

    complete_apps = ['review']
