from django import forms
from .models import *

class UpdateDetailsForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='Surname', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email Address', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    vendor = forms.CharField(label='Vendor', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    platform = forms.CharField(label='Platform', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    api_username = forms.CharField(label='API Username', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    api_password = forms.CharField(label='API Password', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    api_access_token = forms.CharField(label='API Access Token', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

