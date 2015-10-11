from django.conf.urls import patterns, include, url
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

from tastypie.resources import ModelResource
from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie import fields
from tastypie_oauth.authentication import OAuth2ScopedAuthentication, OAuth20Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from provider.constants import READ, WRITE, READ_WRITE

from drsounds.models import *
from qi.cors import *


class APIResource(CORSModelResource):
	def dehydrate(self, bundle):
		bundle.data['type'] = self.Meta.resource_name
		return bundle 		

class ServiceResource(APIResource):
	class Meta:
		detail_uri_name = 'slug'
		model = Service

class ServiceReleaseResource(APIResource):
	service = fields.ForeignKey('drsounds.api.ServiceResource', 'service', full=True, null=True)
	release = fields.ForeignKey('drsounds.api.ReleaseResource', 'release', full=False, null=True)
	identifier = fields.CharField(attribute='identifier', null=True)
	class Meta:
		detail_uri_name = 'slug'
		model = ServiceRelease
		resource_name = 'servicerelease'


class ReleaseResource(APIResource):
	id = fields.CharField(attribute='id')
	artists = fields.ToManyField('drsounds.api.ArtistResource', 'artists', full=True, null=True)
	label = fields.ForeignKey('drsounds.api.LabelResource', 'label', full=True, null=True)
	service_links = fields.ToManyField('drsounds.api.ServiceReleaseResource', 'links', full=True, null=True)
	class Meta:
		queryset = Release.objects.all().order_by('-release_date')
		model = Release
		detail_uri_name = 'upc'
		resource_name = 'release'
		filtering = {
			'artists': ALL_WITH_RELATIONS,
			'label': ALL_WITH_RELATIONS
		}
	def dehydrate(self, bundle):
		bundle.data['slug'] = bundle.data['upc']
		bundle.data['type'] = self.Meta.resource_name
		bundle.data['links'] = {}
	
		return bundle

class ArtistResource(APIResource):
	image_url = fields.FileField(attribute='image_url')
	header_image_url = fields.FileField(attribute='header_image_url')
	class Meta:
		model = Artist
		resource_name = 'artist'
		queryset = Artist.objects.all()
		detail_uri_name = 'slug'


class Universe(APIResource):
	class Meta:
		model = Universe
		resource_name = 'universe'
		queryset = Universe.objects.all()
		detail_uri_name = 'slug'


class Dimension(APIResource):
	universe = fields.ForeignKey('drsounds.api.UniverseResource', 'universe', full=True)
	class Meta:
		model = Dimension
		resource_name = 'dimension'
		queryset = Dimension.objects.all()
		detail_uri_name = 'slug'


class ThemeResource(APIResource):
	compositions = fields.ToManyField('drsounds.api.CompositionResource', 'compositions', full=True, use_in='list', null=True)
	genres = fields.ToManyField('drsounds.api.GenreResource', 'genres', full=True, use_in='list', null=True)
	class Meta:
		model = Theme
		resource_name = 'theme'
		queryset = Theme.objects.all()
		filtering = {
			'compositions': ALL_WITH_RELATIONS,
			'genres': ALL_WITH_RELATIONS
		}
		detail_uri_name = 'slug'


class Software(APIResource):
	class Meta:
		queryset = Mix.objects.all()
		model = Mix
		resource_name = 'software'


class MixResource(APIResource):
	artists = fields.ToManyField('drsounds.api.ArtistResource', 'artists', full=True, null=True)
	class Meta:
		queryset = Mix.objects.all()
		model = Mix
		resource_name = 'mix'


class TrackResource(APIResource):
	artists = fields.ToManyField('drsounds.api.ArtistResource', 'artists', full=True, null=True)
	release = fields.ForeignKey('drsounds.api.ReleaseResource', 'release', full=True, null=True)
	label = fields.ForeignKey('drsounds.api.LabelResource', 'label', full=True, null=True)
	song = fields.ForeignKey('drsounds.api.SongResource', 'song', full=True, null=True)
	class Meta:
		filtering = {
			'artists': ALL_WITH_RELATIONS,
			'release': ALL_WITH_RELATIONS,
			'label': ALL_WITH_RELATIONS
		}
		queryset = Track.objects.all()
		model = Track
		resource_name = 'track'


class SongResource(APIResource):
	artists = fields.ToManyField('drsounds.api.ArtistResource', 'artists', full=True, null=True)
	class Meta:
		queryset = Song.objects.all().order_by('-popularity')
		model = Song
		resource_name = 'song'
		filtering = {
			'artists': ALL,
			'release': ALL
		}



class VideoResource(APIResource):
	artists = fields.ToManyField('drsounds.api.ArtistResource', 'artists', full=True, null=True)
	class Meta:
		filtering = {
			'artists': ALL_WITH_RELATIONS
		}
		queryset = Video.objects.all()
		model = Video
		resource_name = 'video'





class CompositionResource(APIResource):
	artists = fields.ToManyField('drsounds.api.ArtistResource', 'artists', full=True, null=True)
	theme = fields.ForeignKey('drsounds.api.ThemeResource', 'theme', full=True, null=True)
	software = fields.ForeignKey('drsounds.api.SoftwareResource', 'software', full=True, null=True)
	themes = fields.ToManyField('drsounds.api.ThemeResource', 'themes', full=True, null=True)
	melodies = fields.ToManyField('drsounds.api.MelodyResource', 'melodies', full=True, use_in='list', null=True)
	class Meta:
		model = Composition
		resource_name = 'composition'
		queryset = Composition.objects.all().order_by('-created')
		filtering = {
			'theme': ALL_WITH_RELATIONS,
			'themes': ALL_WITH_RELATIONS,
			'artists': ALL_WITH_RELATIONS,
			'melodies': ALL_WITH_RELATIONS
		}
		detail_uri_name = 'slug'


class GenreResource(APIResource):
	class Meta:
		model = Genre
		resource_name = 'genre'
		queryset = Genre.objects.all()


class MelodyResource(APIResource):
	artist = fields.ForeignKey('drsounds.api.ArtistResource', 'artist', full=True, null=True)
	class Meta:
		model = Melody
		resource_name = 'melody'
		filtering = {
			'compositions': ALL_WITH_RELATIONS,
			'artist': ALL_WITH_RELATIONS
		}
		queryset = Melody.objects.all().order_by('-composed')
		detail_uri_name = 'slug'



class LabelResource(APIResource):
	class Meta:
		model = Label
		detail_uri_name = 'slug'
		resource_name = 'label'
		queryset = Label.objects.all()