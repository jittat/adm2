# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ReportCategory'
        db.create_table('result_reportcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('result_set_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('result', ['ReportCategory'])

        # Adding model 'QualifiedApplicant'
        db.create_table('result_qualifiedapplicant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticket_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['result.ReportCategory'])),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Applicant'])),
        ))
        db.send_create_signal('result', ['QualifiedApplicant'])

        # Adding model 'AdmissionRound'
        db.create_table('result_admissionround', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('last_date', self.gf('django.db.models.fields.DateField')()),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('result', ['AdmissionRound'])

        # Adding model 'AdmissionResult'
        db.create_table('result_admissionresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='admission_results', to=orm['application.Applicant'])),
            ('round_number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_admitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_waitlist', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('admitted_major', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application.Major'], null=True)),
            ('additional_info', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('result', ['AdmissionResult'])

        # Adding model 'NIETSScores'
        db.create_table('result_nietsscores', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('applicant', self.gf('django.db.models.fields.related.OneToOneField')(related_name='NIETS_scores', unique=True, to=orm['application.Applicant'])),
            ('score_list', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('result', ['NIETSScores'])


    def backwards(self, orm):
        
        # Deleting model 'ReportCategory'
        db.delete_table('result_reportcategory')

        # Deleting model 'QualifiedApplicant'
        db.delete_table('result_qualifiedapplicant')

        # Deleting model 'AdmissionRound'
        db.delete_table('result_admissionround')

        # Deleting model 'AdmissionResult'
        db.delete_table('result_admissionresult')

        # Deleting model 'NIETSScores'
        db.delete_table('result_nietsscores')


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
        'application.major': {
            'Meta': {'ordering': "['number']", 'object_name': 'Major'},
            'confirmation_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5'})
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
