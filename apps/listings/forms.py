from django.contrib.auth.models import User
from django import forms

class UserForm(forms.Form):
    username = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('This email is already registered.')
        return username
