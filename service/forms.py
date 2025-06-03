from django import forms
from .models import Franchise
import re

class FranchiseForm(forms.ModelForm):
    class Meta:
        model = Franchise
        fields = ['name', 'contact_no', 'email', 'date', 'time', 'address']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and isinstance(email, str):  # NoneType या unexpected type से बचने के लिए
            if not email.endswith('@gmail.com'):
                raise forms.ValidationError("Only Gmail addresses are allowed.")
        else:
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean_contact_no(self):
        contact = self.cleaned_data.get('contact_no')
        pattern = r'^\+91\d{10}$'
        if not re.match(pattern, contact):
            raise forms.ValidationError("Phone number must start with +91 and have 10 digits.")
        return contact
    
    
    # =======franchise model=======================

from .models import Franchiseservice

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Franchiseservice
        fields = ['img1', 'title', 'paragraph', 'description', 'img2']
