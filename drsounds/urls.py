from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from api import *

from tastypie.api import Api
 
v1_api = Api(api_name='v1')
v1_api.register(SongResource())
v1_api.register(CompositionResource())
v1_api.register(ThemeResource())
v1_api.register(GenreResource())
v1_api.register(ReleaseResource())
v1_api.register(ArtistResource())
v1_api.register(MelodyResource())
v1_api.register(LabelResource())
v1_api.register(ThemeResource())
v1_api.register(VideoResource())
v1_api.register(TrackResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/', include(v1_api.urls)),
)