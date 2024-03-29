# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Registration', fields ['activation_key']
        db.create_index('application_registration', ['activation_key'], unique=True)


    def backwards(self, orm):
        
        # Removing index on 'Registration', fields ['activation_key']
        db.delete_index('application_registration', ['activation_key'])


    models = {
        'application.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'road': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'village_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'village_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
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
        'application.applicantaddress': {
            'Meta': {'object_name': 'ApplicantAddress'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'address'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'contact_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'contact_owner'", 'unique': 'True', 'to': "orm['application.Address']"}),
            'home_address': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'home_owner'", 'unique': 'True', 'to': "orm['application.Address']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'application.applyingcondition': {
            'Meta': {'ordering': "['number']", 'object_name': 'ApplyingCondition'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'application.education': {
            'Meta': {'object_name': 'Education'},
            'alt_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'education'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'has_graduated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school_city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'school_province': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'application.gpexamdate': {
            'Meta': {'object_name': 'GPExamDate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month_year': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'application.major': {
            'Meta': {'ordering': "['number']", 'object_name': 'Major'},
            'confirmation_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'application.majorpreference': {
            'Meta': {'object_name': 'MajorPreference'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'preference'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'majors': ('application.fields.IntegerListField', [], {})
        },
        'application.passwordrequestlog': {
            'Meta': {'object_name': 'PasswordRequestLog'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'password_request_log'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_request_at': ('django.db.models.fields.DateTimeField', [], {}),
            'num_requested_today': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'application.personalinfo': {
            'Meta': {'object_name': 'PersonalInfo'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'personal_info'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '35'})
        },
        'application.registration': {
            'Meta': {'ordering': "['-registered_at']", 'object_name': 'Registration'},
            'activation_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registrations'", 'to': "orm['application.Applicant']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'application.submissioninfo': {
            'Meta': {'ordering': "['applicantion_id']", 'object_name': 'SubmissionInfo'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'submission_info'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'applicantion_id': ('django.db.models.fields.AutoField', [], {'unique': 'True', 'primary_key': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_updated_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'paid_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['application']
