# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Applicant'
        db.create_table('application_applicant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('national_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('hashed_password', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('has_logged_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('activation_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_related_model', self.gf('application.fields.IntegerListField')(default=None)),
        ))
        db.send_create_signal('application', ['Applicant'])

        # Adding model 'SubmissionInfo'
        db.create_table('application_submissioninfo', (
            ('applicantion_id', self.gf('django.db.models.fields.AutoField')(unique=True, primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='submission_info', unique=True, to=orm['application.Applicant'])),
            ('salt', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('submitted_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_updated_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal('application', ['SubmissionInfo'])

        # Adding model 'PersonalInfo'
        db.create_table('application_personalinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='personal_info', unique=True, to=orm['application.Applicant'])),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('nationality', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('ethnicity', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('application', ['PersonalInfo'])

        # Adding model 'Address'
        db.create_table('application_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('village_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('village_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('road', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('province', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('application', ['Address'])

        # Adding model 'ApplicantAddress'
        db.create_table('application_applicantaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='address', unique=True, to=orm['application.Applicant'])),
            ('home_address', self.gf('django.db.models.fields.related.OneToOneField')(related_name='home_owner', unique=True, to=orm['application.Address'])),
            ('contact_address', self.gf('django.db.models.fields.related.OneToOneField')(related_name='contact_owner', unique=True, to=orm['application.Address'])),
        ))
        db.send_create_signal('application', ['ApplicantAddress'])

        # Adding model 'GPExamDate'
        db.create_table('application_gpexamdate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month_year', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('application', ['GPExamDate'])

        # Adding model 'Education'
        db.create_table('application_education', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='education', unique=True, to=orm['application.Applicant'])),
            ('has_graduated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('school_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('school_city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('school_province', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('alt_name', self.gf('django.db.models.fields.CharField')(default='', max_length=300, null=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('application', ['Education'])

        # Adding model 'Major'
        db.create_table('application_major', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('confirmation_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('application', ['Major'])

        # Adding model 'MajorPreference'
        db.create_table('application_majorpreference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='preference', unique=True, to=orm['application.Applicant'])),
            ('majors', self.gf('application.fields.IntegerListField')()),
        ))
        db.send_create_signal('application', ['MajorPreference'])

        # Adding model 'Registration'
        db.create_table('application_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registrations', to=orm['application.Applicant'])),
            ('registered_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10, blank=True)),
        ))
        db.send_create_signal('application', ['Registration'])

        # Adding model 'PasswordRequestLog'
        db.create_table('application_passwordrequestlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='password_request_log', unique=True, to=orm['application.Applicant'])),
            ('last_request_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('num_requested_today', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('application', ['PasswordRequestLog'])

        # Adding model 'ApplyingCondition'
        db.create_table('application_applyingcondition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('application', ['ApplyingCondition'])


    def backwards(self, orm):
        
        # Deleting model 'Applicant'
        db.delete_table('application_applicant')

        # Deleting model 'SubmissionInfo'
        db.delete_table('application_submissioninfo')

        # Deleting model 'PersonalInfo'
        db.delete_table('application_personalinfo')

        # Deleting model 'Address'
        db.delete_table('application_address')

        # Deleting model 'ApplicantAddress'
        db.delete_table('application_applicantaddress')

        # Deleting model 'GPExamDate'
        db.delete_table('application_gpexamdate')

        # Deleting model 'Education'
        db.delete_table('application_education')

        # Deleting model 'Major'
        db.delete_table('application_major')

        # Deleting model 'MajorPreference'
        db.delete_table('application_majorpreference')

        # Deleting model 'Registration'
        db.delete_table('application_registration')

        # Deleting model 'PasswordRequestLog'
        db.delete_table('application_passwordrequestlog')

        # Deleting model 'ApplyingCondition'
        db.delete_table('application_applyingcondition')


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
