# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'AdditionalResult.round_number'
        db.add_column('result_additionalresult', 'round_number', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'AdditionalResult.round_number'
        db.delete_column('result_additionalresult', 'round_number')


    models = {
        'application.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'activation_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'additional_hashed_password': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '200'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'has_additional_result': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_related_model': ('application.fields.IntegerListField', [], {'default': 'None'}),
            'hashed_password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'national_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'application.major': {
            'Meta': {'ordering': "['number']", 'object_name': 'Major'},
            'confirmation_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'result.additionalresult': {
            'Meta': {'object_name': 'AdditionalResult'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'additional_result'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'round_number': ('django.db.models.fields.IntegerField', [], {})
        },
        'result.admissionresult': {
            'Meta': {'ordering': "['round_number']", 'object_name': 'AdmissionResult'},
            'additional_info': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'admitted_major': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Major']", 'null': 'True'}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admission_results'", 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_waitlist': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'round_number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'result.admissionround': {
            'Meta': {'ordering': "['-number']", 'object_name': 'AdmissionRound'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_date': ('django.db.models.fields.DateField', [], {}),
            'number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'result.nietsscores': {
            'Meta': {'object_name': 'NIETSScores'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'NIETS_scores'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_request_successful': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'requested_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'score_list': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'result.qualifiedapplicant': {
            'Meta': {'ordering': "['order']", 'object_name': 'QualifiedApplicant'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['application.Applicant']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['result.ReportCategory']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'ticket_number': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'result.reportcategory': {
            'Meta': {'ordering': "['order']", 'object_name': 'ReportCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'result_set_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['result']
