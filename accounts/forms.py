from django import forms
from django.forms import widgets

class ImportContactsForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=widgets.PasswordInput)