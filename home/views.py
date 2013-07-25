import fcntl
import os
#import pycurl
from urllib import urlencode

from util.plots import boxfill as box_fill
from util.plots import getVar as get_var

import proof_of_concept

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,render_to_response
from django.template import Context, loader, RequestContext
from django.conf import settings
from django.utils import simplejson
if not settings.configured:
    settings.configure()

def test_page(request):
    return render_to_response("test.html",None,context_instance=RequestContext(request))

def logout_view(request):
    try:
        logout(request)
    except Exception as e:
        #user has not been logged in.
        #redir to login page
        return HttpResponseRedirect(reverse('login:login'))
        
    return render_to_response('logout.html')


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
            plot_filename = box_fill(myfile, myvar, selection_dict, proxy_cert = active_cert)
            
            if not plot_filename:
                return render_to_response("accessDenied.html",None,context_instance=RequestContext(request))
            
            return render(request, 'boxfill.html', {
                'png': plot_filename,
            })

def make_boxfill(request):
    if not request.user.is_authenticated():
        # send them to the login page, with a ?redir= on the end pointing back to this page
        return HttpResponseRedirect(reverse('login:login') + "?" + urlencode({'redir':reverse('home.views.testplot_form')}))
    else:
        active_cert = settings.PROXY_CERT_DIR + request.user.username + '.pem'
        myfile=request.GET['fnm']
        myvar=request.GET['var']
        print myvar
        n=request.GET['n']
        s=request.GET['s']
        e=request.GET['e']
        w=request.GET['w']
        selection_dict = {'latitude':(int(n),int(s)),'longitude':(int(e),int(w)),'time':slice(0,1)}
        try:
            plot_filename = box_fill(myfile, myvar, selection_dict, proxy_cert = active_cert)
            obj={"png":plot_filename}
            json_res=simplejson.dumps(obj) 
        except Exception, err:
            obj={"png":""}
            json_res=simplejson.dumps(obj) 
        return HttpResponse(json_res, content_type="application/json")


def testplot_form(request,json_param=None):
    if not request.user.is_authenticated():
        # send them to the login page, with a ?redir= on the end pointing back to this page
        return HttpResponseRedirect(reverse('login:login') + "?" + urlencode({'redir':reverse('home.views.testplot_form')}))
    else:
        if request.GET:
            return render(request, 'testplot_form.html', { })
        else:
            #if not json_param:
            #    print "testing through form (no link from ESGF yet)"
            total_plot="4"
            plot_type="boxfill"
            n="-90"
            s="90"
            e="0"
            w="180"
            active_plot="1"

            try:
                myfile=request.POST['file']
                lev1=None
                lev2=None
                if 'lev1' in request.POST:
                    lev1=request.POST['lev1']
                if 'lev2' in request.POST:
                    lev2=request.POST['lev2']
            except:

                return render(request, 'testplot_form.html', {
                    'error_message': "Please fill all required fields",
                })
        
            selection_dict = {
                'latitude':(-90,90),
                'longitude':(0,180),
                'time':slice(0,1)
            }
               
            # tell curl what certificate to use
            #TODO: sanitize request.user.name!
            active_cert = settings.PROXY_CERT_DIR + request.user.username + '.pem'
            varlist=get_var(myfile)
            if not varlist:
                return render_to_response("accessDenied.html",None,context_instance=RequestContext(request))
            """
            if json_param:
                plot_filename = box_fill(myfile, varlist, selection_dict, proxy_cert = active_cert)
            else:
                plot_filename=None
            """
            #plot_filename=settings.MEDIA_URL + "plot-boxfill_httppcmdi9llnlgovthreddsdodsccmip5output1inminmcm41pctco2monatmosamonr1i1p1ccb20130207aggregation1_ccb_latitude_-90_90_longitude_-180_180_time_slice1_6_none_none_none.png"
            mycontent={"curOpt":{"total":total_plot,"type":plot_type,"n":n,"s":s,"e":e,"w":w,"active_plot":active_plot},
                    "dataset":[{"file":myfile,"var":varlist,"id":"2"}],
                    }

            return render(request, 'test_boxfill.html',mycontent)
