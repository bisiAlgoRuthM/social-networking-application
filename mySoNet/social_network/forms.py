from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class SignUpForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta:
    model = User
    fields = ['username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Invalid username or password.')
        return self.cleaned_data
