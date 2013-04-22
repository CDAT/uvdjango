import os

from myproxy_logon import myproxy_logon, GetException

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

import uvdjango.settings as settings

def show_login(request):
    """
    Function to show the login page.
    """
    # for POST requests, attempt logging-in
    if request.POST:
        (is_authenticated, error_msg) = perform_login(request.POST['username'],
                                                        request.POST['password'])
                                                        
        if is_authenticated == False:
            return render_to_response('login_form.html', {
                    'redir': request.POST.get('redir', '..'),
                    'error_message': error_msg,
            }, context_instance = RequestContext(request))
        else:
            # login was successful
            return HttpResponseRedirect('/' + request.POST.get('redir', '..'))
            
    # for GET requests, render the login page
    else:
        return render_to_response('login_form.html', {
                    'redir': request.GET.get('redir', '..')
                }, context_instance = RequestContext(request))

def perform_login(username, password):
    """
    Function to handle authenticating users. It is separate from show_login so
    that it can be easily modified to support other login methods. It is currently
    implemented using myproxy_logon, which retrieves an SSL proxy certificate.
    
    Returns: true if login was successful, false + explanation otherwise
    """
    
    try:
        myproxy_logon(settings.openid_base_url,
                    username,
                    password,
                    os.path.join(settings.proxy_cert_dir,
                                    username + '.pem').encode("UTF-8"),
                    lifetime=43200,
                    port=settings.openid_port
                    )
    except GetException as e:
        error_message = "Invalid username or password."
        return (False, error_message)
    except Exception as e:
        raise e
        
    # if it didn't raise a GetException, login was successful
    return (True, None)