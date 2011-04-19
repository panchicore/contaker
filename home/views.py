from django.template.context import RequestContext
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('index.html', 
                                {'home_active':'active', 'site_location':'Welcome', 'welcome_message':'Welcome to Contaker', },
                                    context_instance=RequestContext(request))