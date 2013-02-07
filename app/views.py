# Create your views here.
import sys
sys.path.append('app/scripts')
from django.http import HttpResponse
from django.template import Context, loader
from django.utils import simplejson
import  sample_plot_function as spf

def hello(request):
    return HttpResponse("Hello World")

def boxfill(request):
    t=loader.get_template("templates/boxfill.html")
    myfile=request.GET['file']
    myvar=request.GET['var']
    latitude_from=int(request.GET['latitude_from'])
    latitude_to=int(request.GET['latitude_to'])
    longitude_from=int(request.GET['longitude_from'])
    longitude_to=int(request.GET['longitude_to'])
    time_slice_from=int(request.GET['time_slice_from'])
    time_slice_to=int(request.GET['time_slice_to'])
    lev1=None
    lev2=None
    if 'lev1' in request.GET:
        lev1=request.GET['lev1']
    if 'lev2' in request.GET:
        lev2=request.GET['lev2']


    selection_dict={'latitude':(latitude_from,latitude_to),'longitude':(longitude_from,longitude_to),'time':slice(time_slice_from,time_slice_to)}
    try:
        nm = spf.plotBoxfill(myfile,myvar,selection_dict)
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
    c=Context({'png':nm})
    return HttpResponse(t.render(c))

