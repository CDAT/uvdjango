from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

def show_index(request):
    return render_to_response('index.html', {
                }, context_instance = RequestContext(request))