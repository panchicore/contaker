from django.template.context import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django_open_inviter.open_inviter import OpenInviter
from contacts.models import Contact
from errors.views import general_error

@login_required
def user_settings(request):
    return render_to_response('accounts/profile.html', {'accounts_active':'active', 'user':request.user },
                          context_instance=RequestContext(request))

def user_login(request):
    try:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)

            if form.is_valid():
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return general_error(request, title='Error Login', message='Invalid Authentication', redirect='accounts.views.user_login')
            else:
                return general_error(request, title='Error Login', message='Invalid Authentication Form', redirect='accounts.views.user_login')
        else:
            form = AuthenticationForm()

            return render_to_response('accounts/login.html', {'accounts_active':'active', 'form':form},
                                  context_instance=RequestContext(request))
    except Exception, e:
        return general_error(request, title='Error Login', message=e.message, redirect='accounts.views.user_login')

@login_required
def user_logout(request):
    if request.user is not None:
        logout(request)

    return HttpResponseRedirect(reverse('home'))

def user_register(request):
    try:
        if request.method == 'POST':
            user = User.objects.create_user(request.POST['username'], '', request.POST['password1'])
            user.save()

            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)

            return HttpResponseRedirect(reverse('dashboard'))
        else:
            form = UserCreationForm()
            return render_to_response('accounts/register.html', {'accounts_active':'active', 'form':form},
                                  context_instance=RequestContext(request))
    except Exception, e:
        return general_error(request, title='Error Registering', message=e.message, redirect='accounts.views.user_register')

@login_required
def import_contacts(request):
    try:
        if request.method == 'POST':
            from accounts.forms import ImportContactsForm
            form = ImportContactsForm(data=request.POST)

            if form.is_valid():
                o = OpenInviter()
                contacts = o.contacts(request.POST['email'], request.POST['password'])

                total = len(contacts)

                if contacts is not None:
                    return render_to_response('accounts/contacts.html', {'accounts_active':'active', 'contacts':contacts, 'total':total, },
                                            context_instance=RequestContext(request))
                else:
                    return HttpResponseRedirect(reverse('accounts'))
            else:
                return general_error(request, title='Error Importing Contacts', message='Invalid Authentication Form', redirect='accounts.views.import_contacts')
        else:
            from accounts.forms import ImportContactsForm
            form = ImportContactsForm()

            return render_to_response('accounts/import.html', {'accounts_active':'active', 'form':form, },
                                        context_instance=RequestContext(request))
    except Exception, e:
        return general_error(request, title='Error Importing Contacts', message=e.message, redirect='accounts.views.import_contacts')
    
@login_required
def update_contacts(request):
    if request.method == 'POST':
        for i in range(int(request.POST['total_contacts'])):
            try:
                c = Contact()

                c.user = request.user
                c.name = request.POST['name' + str(i)]
                c.email = request.POST['email' + str(i)]

                c.save()
            except Exception:
                print 'none'

        return HttpResponseRedirect(reverse('dashboard'))
    else:
            return HttpResponseRedirect(reverse('accounts'))