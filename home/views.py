import proof_of_concept

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from django.conf import settings
if not settings.configured:
    settings.configure()

def show_index(request):
    return render_to_response('index.html', {
                }, context_instance = RequestContext(request))

def boxfill(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login-login', args={'redir':reverse('home.views.boxfill')}))
    else:
        if request.GET:
            return render_to_response('boxfill_form.html', {
                    }, context_instance = RequestContext(request))
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
                return render_to_response('boxfill_form.html', {
                    'error_message': "Please fill all required fields",
                }, context_instance=RequestContext(request))
        
            selection_dict = {
                'latitude':(latitude_from,latitude_to),
                'longitude':(longitude_from,longitude_to),
                'time':slice(time_slice_from,time_slice_to)
            }
            
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
            return render_to_response('boxfill.html', {
                'png': nm,
            }, context_instance=RequestContext(request))
