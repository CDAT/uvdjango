import cdms2
import vcs
x=vcs.init()
import sys
from django.utils import simplejson
import os

outpth = "app/media/"
def plotBoxfill(file,var,selection,lev1=None,lev2=None):
    f=cdms2.open(file)
    s=f(var,**selection)
    b=x.createboxfill()
    if lev1 is not None and lev2 is not None:
        b.level_1=lev1
        b.level_2=lev2
    x.plot(s,b,bg=1,ratio='autot') # plots in bg
    nm = "plotBoxfill_%s_%s_%s_%s_%s" % (file,var,repr(selection),lev1,lev2)
    nm=nm.replace(":","")
    nm=nm.replace("/","")
    nm=nm.replace("'","")
    nm=nm.replace("{","")
    nm=nm.replace("}","")
    nm=nm.replace(" ","")
    print "Outputed to %s/%s" % (os.getcwd(),nm)
    x.png(outpth+nm)
    return nm


if __name__ == "__main__":
    file = "http://esg-datanode.jpl.nasa.gov/thredds/dodsC/esg_dataroot/obs4MIPs/observations/atmos/husNobs/mon/grid/NASA-JPL/AIRS/v20110608/husNobs_AIRS_L3_RetStd-v5_200209-201105.nc"
    var = "husNobs"
    selection = {'latitude':(-10,20),'longitude':(-180,180),'time':slice(1,6)}
    plotBoxfill(file,var,selection)
