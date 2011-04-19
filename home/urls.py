from django.conf.urls.defaults import *

urlpatterns = patterns ('',
    url(r'^$', 'home.views.index', name='home')
)