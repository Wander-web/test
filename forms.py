from django import forms
from django.contrib.auth.models import User
from . import models


class SubjUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password',
                  ]
        widgets = {'password': forms.PasswordInput()}


class SubjForm(forms.ModelForm):
    class Meta:
        model = models.Subj
        fields = ['prof_real', 'prof_intellect', 'prof_social',
                  'prof_conventional', 'prof_initiative', 'prof_art']
