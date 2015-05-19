from django.conf.urls import patterns, include, url
from qi.views import *
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leros.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'qi.views.dashboard'),
    url(r'^accounts/(?P<id>([\w\-]+))/$', 'qi.views.account'),
    url(r'^accounts/$', AccountList.as_view()),
)
