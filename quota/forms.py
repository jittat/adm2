from models import AdditionalEducation
from django import forms

class QuotaForm(forms.ModelForm):
    class Meta:
        model = AdditionalEducation
        exclude = ['applicant']
