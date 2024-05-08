from django import forms
from .models import Patient
from .models import RiskAssessment


class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['risk_factors']


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'phone_number', 'address', 'medical_documents']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
