from contacts.models import Contact, ContactSchedules
from django import forms


class NewContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ('user', 'is_active',)


class NewScheduleForm(forms.ModelForm):
    
    class Meta:
        model = ContactSchedules
        exclude = ('user',)

    def __init__(self, user=None, **kwargs):
        super(NewScheduleForm, self).__init__(**kwargs)
        if user:
            self.fields['contact_to'].queryset = Contact.objects.filter(user=user)