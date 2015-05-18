from django.conf.urls import patterns, include, url
from qi.views import *
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
 
v1_api = Api(api_name='v1')
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leros.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'accounting.views.dashboard'),
)
