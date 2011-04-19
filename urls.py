from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

handler404 = 'errors.views.http404'
handler500 = 'errors.views.http500'

urlpatterns = patterns('',
    url(r'^$', include('home.urls')),
    #url(r'^dashboard/', include('contacts.urls')),
    url(r'^dashboard/$', 'contacts.views.dashboard', name='dashboard'),

    url(r'^contacts/new/$', 'contacts.views.new_contact', name='new_contact'),
    url(r'^contacts/(?P<contact_id>\d+)/$', 'contacts.views.view_contact', name='view_contact'),
    url(r'^contacts/(?P<contact_id>\d+)/edit/$', 'contacts.views.edit_contact', name='edit_contact'),
    url(r'^contacts/(?P<contact_id>\d+)/delete/$', 'contacts.views.delete_contact', name='delete_contact'),

    url(r'^schedules/new/$', 'contacts.views.new_schedule', name='new_schedule'),
    url(r'^schedules/(?P<schedule_id>\d+)/$', 'contacts.views.view_schedule', name='view_schedule'),
    url(r'^schedules/(?P<schedule_id>\d+)/edit/$', 'contacts.views.edit_schedule', name='edit_schedule'),
    url(r'^schedules/(?P<schedule_id>\d+)/delete/$', 'contacts.views.delete_schedule', name='delete_schedule'),
    url(r'^accounts/', include('accounts.urls')),
    #url(r'^support/', include('support.urls'), name='support'),

    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),
)