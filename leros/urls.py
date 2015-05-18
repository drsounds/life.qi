from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from leros.api import *
 
v1_api = Api(api_name='v1')
v1_api.register(ActivityResource())
v1_api.register(FacilityResource())
v1_api.register(SportResource())
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leros.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'leros.views.dashboard'),
    url(r'^activity/$', 'leros.views.activitys'),
    url(r'^activity/add/$', 'leros.views.add_activity'),
    url(r'^activity/edit/(?P<id>\w+)/$', 'leros.views.edit_activity'),
    url(r'^activity/view/(?P<id>\w+)/$', 'leros.views.view_activity'),
    url(r'^activity/delete/(?P<id>\w+)/$', 'leros.views.delete_activity'),
    url(r'^booking/add/$', 'leros.views.add_booking'),
    url(r'^booking/delete/(?P<id>\w+)/$', 'leros.views.delete_booking'),
    url(r'^booking/edit/(?P<id>\w+)/$', 'leros.views.edit_booking'),
    url(r'^booking/(?P<booking_id>\w+)/$', 'leros.views.booking'),
    url(r'^booking/$', 'leros.views.bookings'),
)
