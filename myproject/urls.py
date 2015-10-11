from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from qi.api import *

from tastypie.api import Api
 
v1_api = Api(api_name='v1')
v1_api.register(QiResource())
v1_api.register(TransactionResource())
v1_api.register(AccountResource())
v1_api.register(CurrencyResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^qi/', include('qi.urls')),
	url(r'^oauth/', include('provider.oauth2.urls', namespace = 'oauth2')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^drsounds/', include('drsounds.urls')),
)