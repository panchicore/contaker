from django_extensions.db.fields import ModificationDateTimeField
from django_extensions.db.fields import CreationDateTimeField
from django.contrib.auth.models import User
from django import forms

from django.db import models

class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(is_active=1)

class Contact(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telephone = models.IntegerField(max_length=12, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return self.name

class ContactHistory(models.Model):
    user = models.ForeignKey(User)
    contact = models.ForeignKey(Contact, related_name='histories')
    action = models.CharField(max_length=255, choices=( ('called','called'),('wrote','wrote'), ('added','added'), ('edited','edited'),('deleted','deleted') ) )

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return 'I %s %s' % (self.action, self.contact.name)

class ContactSchedules(models.Model):
    user = models.ForeignKey(User)
    task = models.CharField(max_length=255, choices=(('call', 'call'), ('write', 'write'), ('alert', 'alert')))
    #contact_to = models.IntegerField(max_length=12, null=True, blank=True)
    contact_to = models.ForeignKey(Contact)
    date_alert = models.DateTimeField()
    
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return '%s %s at %s' % (self.task, self.contact_to, self.date_alert)