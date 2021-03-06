from django.shortcuts import render_to_response
from django.template.context import RequestContext

def http404(request):
    return render_to_response("errors/404.html", {'site_location':'Error 404', },
                              context_instance=RequestContext(request))

def http500(request):
    return render_to_response("errors/500.html", {'site_location':'Error 500', },
                              context_instance=RequestContext(request))

def general_error(request, title, message, redirect):
    return render_to_response("errors/general.html", {'site_location':'Error', 'title':title, 'message':message, 'redirect':redirect },
                              context_instance=RequestContext(request))