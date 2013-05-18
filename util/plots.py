import cdms2
from fcntl import flock, LOCK_EX, LOCK_UN
import os
import pycurl
import sys
import vcs

from util.sanitize import sanitize_filename

from django.conf import settings
if not settings.configured:
    settings.configure()
    
def boxfill(in_file, variable, in_selection, proxy_cert=None, lev1=None, lev2=None):
    '''
    Generates a boxfill plot of the selected variable.
    Writes a .png file to disk and returns the URL to it when it's done.
    '''
    ### determine the filename plot will have ###
    filename = "plot-boxfill_%s_%s_%s_%s_%s" % (in_file, variable, str(in_selection), lev1, lev2)
    filename = sanitize_filename(filename)
    print filename
    print settings.MEDIA_ROOT
    filepath = os.path.join(settings.MEDIA_ROOT, filename)
    print filepath
    
    ### check to see if we've already created this file ###
    if(os.path.isfile(filepath)):
        return settings.MEDIA_URL + filename
    
    ### if not, create the plot, write it to file, and return ###
    try:
        curl = pycurl.Curl()
        if os.path.isfile(proxy_cert):
            print "\n\nSETTING PYCURL OPTIONS\n\n"
            curl.setopt(pycurl.SSLKEY, str(proxy_cert))
            curl.setopt(pycurl.SSLCERT, str(proxy_cert))
            curl.setopt(pycurl.SSL_VERIFYPEER, 1)
            curl.setopt(pycurl.SSL_VERIFYHOST, 1)
            curl.setopt(pycurl.CAPATH, '/export/fedorthurman1/.certificates/')
            curl.setopt(pycurl.CAINFO, '/export/fedorthurman1/.certificates/GlobusSimpleCA.pem')
            print proxy_cert
        else:
            print "\n\nFAILED TO SET PYCURL OPTIONS\n\n"
            
        data = cdms2.open(in_file)
        selection = data(variable, **in_selection)
        canvas = vcs.init()
        plot = canvas.createboxfill()
        if lev1 is not None and lev2 is not None:
            plot.level_1 = lev1
            plot.level_2 = lev2
        canvas.clear()
        canvas.plot(selection, plot, bg=1, ratio='autot') # plots in background
        
        with open(filepath, 'wb') as outfile:
            flock(outfile, LOCK_EX)
            canvas.png(filepath)
            flock(outfile, LOCK_UN)
        return filename + ".png"
    except Exception as e:
        print type(e)
        print "An exception has occured in plots.boxfill()! The error was \"%s\"" % e
        return None