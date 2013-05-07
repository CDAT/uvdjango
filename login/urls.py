from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from login import views

urlpatterns = patterns('login.views',
        # /
        url(r'^/?$', 'show_login', name='login'),
)