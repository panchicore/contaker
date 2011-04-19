from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from contacts.forms import NewContactForm, NewScheduleForm
from contacts.models import Contact, ContactSchedules, ContactHistory
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

@login_required
def dashboard(request):
    contacts = Contact.active.filter(user=request.user)
    schedules = ContactSchedules.objects.filter(user=request.user)
    histories = ContactHistory.objects.filter(user=request.user)
    
    return render_to_response('contacts/dashboard.html', {'dashboard_active':'active', 'contacts':contacts, 'schedules':schedules, 'histories':histories },
                                context_instance=RequestContext(request))

@login_required
def view_contact(request, contact_id):
    c = get_object_or_404(Contact, id=contact_id, user=request.user)

    ch = ContactHistory()
    ch.user = request.user
    ch.action = 'viewed'
    ch.contact = Contact.active.get(id=c.id)
    ch.save()
    
    return render_to_response('contacts/view_contact.html', {'dashboard_active':'active', 'contact':c},
                              context_instance=RequestContext(request))

@login_required
def view_schedule(request, schedule_id):
    cs = get_object_or_404(ContactSchedules, id=schedule_id, user=request.user)
    return render_to_response('contacts/view_schedule.html', {'dashboard_active':'active', 'schedule':cs},
                              context_instance=RequestContext(request))

@login_required
def new_contact(request):
    if request.method == 'POST':
        form = NewContactForm(request.POST)
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.user = request.user
            new_contact.save()

            ch = ContactHistory()
            ch.user = request.user
            ch.action = 'added'
            ch.contact = Contact.active.get(name=request.POST['name'])
            ch.save()

            messages.success(request, "new contact added")


            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = NewContactForm()
    return render_to_response('contacts/new_contact.html', {'dashboard_active':'active', 'form':form},
                                context_instance=RequestContext(request))

@login_required
def edit_contact(request, contact_id):
    if request.method == 'POST':
        form = NewContactForm(data=request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.id = contact_id
            c.user_id = request.user.id
            c.save()

            ch = ContactHistory()
            ch.user = request.user
            ch.action = 'edited'
            ch.contact = Contact.active.get(id=c.id)
            ch.save()

            messages.success(request, "contact edited")
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        c = get_object_or_404(Contact, id=contact_id, user=request.user)
        form = NewContactForm(instance=c)
        
        return render_to_response('contacts/edit_contact.html', {'dashboard_active':'active', 'form':form, 'contact':c},
                                    context_instance=RequestContext(request))

@login_required
def delete_contact(request, contact_id):
    c = get_object_or_404(Contact, id=contact_id, user=request.user)

    if request.method == 'POST':
        c.delete()
        
        messages.success(request, 'contact deleted')
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render_to_response('contacts/delete_contact.html', {'dashboard_active':'active', 'contact':c},
                                  context_instance=RequestContext(request))

@login_required
def new_schedule(request):
    if request.method == 'POST':
        form = NewScheduleForm(data=request.POST)
        if form.is_valid():
            new_schedule = form.save(commit=False)
            new_schedule.user = request.user
            new_schedule.save()
            messages.success(request, 'new schedule added')
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = NewScheduleForm(request.user)
        #form.fields['contact_to'].queryset = Contact.objects.filter(user=request.user)

    return render_to_response('contacts/new_schedule.html', {'dashboard_active':'active', 'form':form},
                                context_instance=RequestContext(request))

@login_required
def edit_schedule(request, schedule_id):
    if request.method == 'POST':
        form = NewScheduleForm(data=request.POST)
        if form.is_valid():
            cs = form.save(commit=False)
            cs.id = schedule_id
            cs.user_id = request.user.id
            cs.save()

            messages.success(request, "schedule edited")
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        cs = get_object_or_404(ContactSchedules, id=schedule_id, user=request.user)
        form = NewScheduleForm(instance=cs)

        return render_to_response('contacts/edit_schedule.html', {'dashboard_active':'active', 'form':form, 'schedule':cs},
                                    context_instance=RequestContext(request))

@login_required
def delete_schedule(request, schedule_id):
    cs = ContactSchedules.objects.get(id=schedule_id, user=request.user)
    cs.delete()
    messages.success(request, 'schedule deleted')
    return HttpResponseRedirect(reverse('dashboard'))