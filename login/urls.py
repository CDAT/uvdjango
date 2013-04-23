from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('login.views',
        # /
        url(r'^/?$', 'show_login', name='login-login'),
)