from django import forms
from django.forms.extras import widgets

class ImportContactsForm(forms.Form):
    mail = forms.EmailField()
    password = forms.CharField(widget=widgets.PasswordInput())