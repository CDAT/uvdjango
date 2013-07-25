from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('home.views',
        # /
        url(r'^plot/boxfill', 'make_boxfill'),
        url(r'^testboxfill/(?P<json_param>)\w*$', 'testplot_form'),
        url(r'^testplot/$', 'testplot_form'),
        url(r'test.html', 'test_page'),
        url(r'^/?$', 'show_index'),
        url(r'^logout/$', 'logout_view'),
        url(r'^boxfill/$', 'boxfill'),
        )

