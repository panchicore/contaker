from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    url(r'^$', 'user_settings', name='accounts'),
    url(r'^import/$', 'import_contacts', name='import_contacts'),
    url(r'^update/$', 'update_contacts', name='update_contacts'),
    url(r'^login/$', 'user_login', name='login'),
    url(r'^logout/$', 'user_logout', name='logout'),
    url(r'^register/$', 'user_register', name='register'),
)