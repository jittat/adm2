# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AdmissionMajorPreference'
        db.create_table('confirmation_admissionmajorpreference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='admission_major_preferences', to=orm['application.Applicant'])),
            ('round_number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_accepted_list', self.gf('application.fields.IntegerListField')()),
            ('is_nomove_request', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ptype', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('confirmation', ['AdmissionMajorPreference'])

        # Adding model 'AdmissionConfirmation'
        db.create_table('confirmation_admissionconfirmation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='admission_confirmations', to=orm['application.Applicant'])),
            ('round_number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('paid_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('confirmed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('confirmation', ['AdmissionConfirmation'])

        # Adding model 'AdmissionWaiver'
        db.create_table('confirmation_admissionwaiver', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='admission_waiver', unique=True, to=orm['application.Applicant'])),
            ('is_waiver', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waived_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('editted_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('confirmation', ['AdmissionWaiver'])

        # Adding model 'StudentRegistration'
        db.create_table('confirmation_studentregistration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='student_registration', unique=True, to=orm['application.Applicant'])),
            ('passport_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('english_first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('english_last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('religion', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('birth_place', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('home_phone_number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('cell_phone_number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('father_title', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('father_first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('father_last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('father_national_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('mother_title', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('mother_first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mother_last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('mother_national_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('confirmation', ['StudentRegistration'])

        # Adding model 'Round2ApplicantConfirmation'
        db.create_table('confirmation_round2applicantconfirmation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='round2_confirmation', unique=True, to=orm['application.Applicant'])),
            ('submitted_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_applying_for_survey_engr', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('confirmation', ['Round2ApplicantConfirmation'])


    def backwards(self, orm):
        
        # Deleting model 'AdmissionMajorPreference'
        db.delete_table('confirmation_admissionmajorpreference')

        # Deleting model 'AdmissionConfirmation'
        db.delete_table('confirmation_admissionconfirmation')

        # Deleting model 'AdmissionWaiver'
        db.delete_table('confirmation_admissionwaiver')

        # Deleting model 'StudentRegistration'
        db.delete_table('confirmation_studentregistration')

        # Deleting model 'Round2ApplicantConfirmation'
        db.delete_table('confirmation_round2applicantconfirmation')


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
            'Meta': {'object_name': 'StudentRegistration'},
            'applicant': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'student_registration'", 'unique': 'True', 'to': "orm['application.Applicant']"}),
            'birth_place': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cell_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'english_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'english_last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'father_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'father_last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'father_national_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'father_title': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'home_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mother_first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mother_last_name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'mother_national_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'mother_title': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'passport_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['confirmation']
