from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('home.views',
        # /
        url(r'^/?$', 'show_index'),
)