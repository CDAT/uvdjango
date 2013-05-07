import pycurl
from urllib import urlencode

import proof_of_concept

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader, RequestContext
from django.conf import settings
if not settings.configured:
    settings.configure()

def show_index(request):
    return render(request, 'index.html', { })

def boxfill(request):
    if not request.user.is_authenticated():
        # send them to the login page, with a ?redir= on the end pointing back to this page
        return HttpResponseRedirect(reverse('login:login') + "?" + urlencode({'redir':reverse('home.views.boxfill')}))
    else:
        if request.GET:
            return render(request, 'boxfill_form.html', { })
        else:
            try:
                myfile=request.POST['file']
                myvar=request.POST['var']
                latitude_from=int(request.POST['latitude_from'])
                latitude_to=int(request.POST['latitude_to'])
                longitude_from=int(request.POST['longitude_from'])
                longitude_to=int(request.POST['longitude_to'])
                time_slice_from=int(request.POST['time_slice_from'])
                time_slice_to=int(request.POST['time_slice_to'])
                lev1=None
                lev2=None
                if 'lev1' in request.POST:
                    lev1=request.POST['lev1']
                if 'lev2' in request.POST:
                    lev2=request.POST['lev2']
            except:
                return render(request, 'boxfill_form.html', {
                    'error_message': "Please fill all required fields",
                })
        
            selection_dict = {
                'latitude':(latitude_from,latitude_to),
                'longitude':(longitude_from,longitude_to),
                'time':slice(time_slice_from,time_slice_to)
            }
               
            # tell curl what certificate to use
            #TODO: sanitize request.user.name!
            active_cert = settings.PROXY_CERT_DIR + request.user.username + '.pem'
            curl = pycurl.Curl()
            curl.setopt(pycurl.SSLKEY, str(active_cert))
            curl.setopt(pycurl.SSLCERT, str(active_cert))

            
            try:
                nm = proof_of_concept.plotBoxfill(myfile,myvar,selection_dict)
                nm=nm.replace(":","")
                nm=nm.replace("/","")
                nm=nm.replace("'","")
                nm=nm.replace("{","")
                nm=nm.replace("}","")
                nm=nm.replace(" ","")
            except Exception, e:
                nm=str(e)
                pass
            #nm = "plotBoxfill_%s_%s_%s_%s_%s" % (myfile,myvar,repr(selection_dict),lev1,lev2)
            #print nm
            return render(request, 'boxfill.html', {
                'png': nm,
            })
