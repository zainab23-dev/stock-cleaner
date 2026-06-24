from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Preference

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ['theme', 'grid_page_size', 'email_notifications']
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-select'}),
            'grid_page_size': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 200}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
