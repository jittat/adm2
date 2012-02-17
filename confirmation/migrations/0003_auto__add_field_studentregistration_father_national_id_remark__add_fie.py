# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'StudentRegistration.father_national_id_remark'
        db.add_column('confirmation_studentregistration', 'father_national_id_remark', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'StudentRegistration.mother_national_id_remark'
        db.add_column('confirmation_studentregistration', 'mother_national_id_remark', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'StudentRegistration.father_national_id_remark'
        db.delete_column('confirmation_studentregistration', 'father_national_id_remark')

        # Deleting field 'StudentRegistration.mother_national_id_remark'
        db.delete_column('confirmation_studentregistration', 'mother_national_id_remark')


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
        'confirmation.admissionconfirmation': {
            'Meta': {'ordering': "['-confirmed_at']", 'object_name': 'AdmissionConfirmation'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admission_confirmations'", 'to': "orm['application.Applicant']"}),
            'confirmed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round_number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'confirmation.admissionmajorpreference': {
            'Meta': {'ordering': "['-round_number']", 'object_name': 'AdmissionMajorPreference'},
            'applicant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'admission_major_preferences'", 'to': "orm['application.Applicant']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted_list': ('application.fields.IntegerListField', [], {}),
            'is_nomove_request': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ptype': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'round_number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'confirmation.admissionwaiver': {
            'Meta': {'object_name': 'AdmissionWaiver'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'admission_waiver'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'editted_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_waiver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waived_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'confirmation.round2applicantconfirmation': {
            'Meta': {'object_name': 'Round2ApplicantConfirmation'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'round2_confirmation'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_applying_for_survey_engr': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'submitted_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'confirmation.studentregistration': {
            'GPA': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'StudentRegistration'},
            'address_avenue': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'student_registration'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cell_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'english_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'english_last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'father_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'father_last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'father_national_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'father_national_id_remark': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'father_title': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'home_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mother_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mother_last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'mother_national_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'mother_national_id_remark': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'mother_title': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'passport_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school_type': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['confirmation']
