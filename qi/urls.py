from django.conf.urls import patterns, include, url
from qi.views import *
from qi.api import *
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
 
v1_api = Api(api_name='v1')
v1_api.register(QiResource())
v1_api.register(TransactionResource())
v1_api.register(AccountResource())
v1_api.register(CurrencyResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leros.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'qi.views.dashboard'),
    url(r'^accounts/(?P<id>([\w\-]+))/$', 'qi.views.account'),
    url(r'^accounts/$', AccountList.as_view()),
    url(r'^api/', include(v1_api.urls)),
)
