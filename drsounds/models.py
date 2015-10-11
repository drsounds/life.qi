from django.db import models
from django.contrib.auth.models import User
import datetime
import string

def _id_generator(size=6, chars=string.ascii_uppercase + string.digits):	
	''' @from http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python '''
	return ''.join(random.choice(chars) for _ in range(size))


class ImageModel(models.Model):
	image_url = models.ImageField(upload_to='images/', blank=True, null=True)
	header_image_url = models.ImageField(upload_to='images/', blank=True, null=True)
	class Meta:
		abstract = True

class SlugModel(models.Model):
	'''
	Slug model
	'''
	slug = models.SlugField(blank=True)
	name = models.CharField(max_length=255)
	description = models.TextField(null=True, blank=True)

	class Meta:
		abstract = True

	def save(self, *args, **kwargs):
		if self.id is None:
			if not self.slug:
				self.slug = _id_generator(6)
		super(SlugModel, self).save(args, kwargs)

	def __unicode__(self):
		return self.name


class Universe(SlugModel):
	pass


class Tag(SlugModel):
	pass


class YinYangModel(models.Model):
	yin = models.FloatField(default=0.5)
	yang = models.FloatField(default=0.5)
	class Meta:
		abstract = True


class Dimension(YinYangModel, SlugModel):
	universe = models.ForeignKey(Universe)

	def is_dark_world(self):
		'''
		Returns if is a dark world (a.ka. entropic world)
		'''
		return yin > 0.5 or yang > 0.5

class Composer(models.Model):
	name = models.CharField(max_length=255)
	user = models.ForeignKey(User)
	def __unicode__(self):
		return self.name


class Channel(models.Model):
	name = models.CharField(max_length=255)
	def __unicode__(self):
		return self.name


class Video(models.Model):
	name = models.CharField(max_length=255)
	artists = models.ManyToManyField('Artist')
	song = models.ForeignKey('Song')
	embed_url = models.URLField()
	def __unicode__(self):
		return self.name


class Show(models.Model):
	name = models.CharField(max_length=255)
	channel = models.ForeignKey(Channel)
	def __unicode__(self):
		return self.name


class Episode(models.Model):
	name = models.CharField(max_length=255)
	show = models.ForeignKey(Show)
	def __unicode__(self):
		return self.name

class Artist(SlugModel, ImageModel):
	user = models.ForeignKey(User, blank=True, null=True)
	genres = models.ManyToManyField('Genre', blank=True, null=True)
	def __unicode__(self):
		return self.name

class MelodyStyle(models.Model):
	name = models.CharField(max_length=255)
	def __unicode__(self):
		return self.name


class Melody(models.Model):
	slug = models.SlugField(blank=True, default=True)
	name = models.CharField(max_length=255)
	composed = models.DateTimeField(default=datetime.datetime.now)
	user = models.ForeignKey(User)
	artist = models.ForeignKey(Artist, related_name='melody')
	composers = models.ManyToManyField(Composer, related_name='melodies')
	style = models.ForeignKey(MelodyStyle, related_name='melody')
	midi_file = models.FileField(null=True, blank=True, upload_to='midi/')
	moments = models.ManyToManyField('Moment', null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	def __unicode__(self):
		return self.name


class Theme(models.Model):
	parent = models.ForeignKey('self', null=True, blank=True)
	slug = models.SlugField(blank=True, default=True)
	name = models.CharField(max_length=255)
	user = models.ForeignKey(User)
	artists = models.ManyToManyField(Artist, related_name='themes')
	genres = models.ManyToManyField('Genre', related_name='themes')
	moments = models.ManyToManyField('Moment', null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	def __unicode__(self):
		return self.name


class Genre(models.Model):
	name = models.CharField(max_length=255)
	def __unicode__(self):
		return self.name


class Software(SlugModel):
	pass



class Composition(models.Model):	
	slug = models.SlugField(blank=True, default=True)
	name = models.CharField(max_length=255)
	artists = models.ManyToManyField(Artist, related_name='compositions')
	melodies = models.ManyToManyField(Melody, related_name='compositions')
	theme = models.ForeignKey(Theme)
	themes = models.ManyToManyField(Theme, related_name='compositions', null=True, blank=True)
	created = models.DateField(default=datetime.datetime.now)
	studio_file = models.FileField(null=True, blank=True, upload_to='compositions/')
	moments = models.ManyToManyField('Moment', null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	software = models.ForeignKey(Software, null=True, blank=True)
	def __unicode__(self):
		return self.name

class Assembly(models.Model):
	song = models.ForeignKey("Song")
	composition = models.ForeignKey("Composition")


class Song(models.Model):
	artists = models.ManyToManyField(Artist)
	name = models.CharField(max_length=255)
	composition = models.ForeignKey(Composition)
	compositions = models.ManyToManyField(Composition, related_name='compositions', null=True, blank=True)
	studio_file = models.FileField(null=True, blank=True, upload_to='melodies/')
	description = models.TextField(null=True, blank=True)
	def __unicode__(self):
		return self.name


class Epoch(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()
	start = models.DateField()
	end = models.DateField()
	user = models.ForeignKey(User)
	description = models.TextField()
	tags = models.ManyToManyField(Tag)


class Track(models.Model):
	name = models.CharField(max_length=255)
	user = models.ForeignKey(User)
	artists = models.ManyToManyField(Artist)
	song = models.ForeignKey(Song)
	isrc = models.CharField(max_length=13, unique=True)
	url = models.CharField(max_length=255)
	moments = models.ManyToManyField('Moment', null=True, blank=True)
	def title(self):
		return '%s (%s)' % (self.song.name, self.name)

	def __unicode__(self):
		return self.title()


class Mix(models.Model):
	artists = models.ManyToManyField(Artist)
	tracks = models.ForeignKey(Track)
	name = models.CharField(max_length=255)
	def __unicode__(self):
		return self.name


class Label(models.Model):
	slug = models.SlugField()
	name = models.CharField(max_length=255)
	def __unicode__(self):
		return self.name


class Service(SlugModel):
	pass


class ServiceRelease(models.Model):
	service = models.ForeignKey('Service')
	release = models.ForeignKey('Release')
	identifier = models.CharField(max_length=255)


class Moment(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField()


class ReleaseTrack(models.Model):
	release = models.ForeignKey('Release')
	track = models.ForeignKey('Track')
	number = models.IntegerField(default=1)
	class Meta:
		db_table = 'drsounds_release_tracks'

class Release(SlugModel):
	artists = models.ManyToManyField(Artist)
	tracks = models.ManyToManyField(Track, null=True, blank=True, through='ReleaseTrack')
	upc = models.CharField(max_length=13)
	release_date = models.DateField(default=datetime.datetime.now)
	label = models.ForeignKey(Label, null=True, blank=True)
	moments = models.ManyToManyField('Moment', null=True, blank=True)
	links = models.ManyToManyField('Service', through='ServiceRelease', null=True, blank=True)
	image_url = models.ImageField(upload_to='images		/', blank=True, null=True)
	header_image_url = models.ImageField(upload_to='images/', blank=True, null=True)
	def __unicode__(self):
		return self.name


class RelationType(models.Model):
	slug = models.CharField(max_length=255, primary_key=True)


class Relation(models.Model):
	relation_type = models.ForeignKey(RelationType)
	source = models.IntegerField()
	target = models.IntegerField()
	source_type = models.CharField(max_length=25)
	target_type = models.CharField(max_length=25)


class Airplay(models.Model):
	time = models.DateTimeField()
	Track = models.ForeignKey(Track)
	episode = models.ForeignKey(Episode)

class QuickTrack(SlugModel):
	isrc = models.CharField(max_length=255)
	artists = models.ManyToManyField(Artist)
	composers = models.ManyToManyField(Composer)
	style = models.ForeignKey(MelodyStyle)
	version = models.CharField(max_length=255, default='Original Edit')
	created = models.DateField()
	software = models.ForeignKey(Software)
	isrc = models.CharField(max_length=13)
	def save(self, *args, **kwargs):
		# First create melody
		self.id = 1
		mel = Melody
		melody = Melody(
			name=self.name, 
			slug=self.slug, 
			artists=self.artists, 
			user=User.objects.get(id=1),
			style=self.style,
			composed=self.created,
			description=self.description
		)
		melody.save()

		theme = Theme(
			name=self.name,
			slug=self.slug,
			artists=self.artists,
			composers=self.composers,
			user=User.objects.get(id=1),
			description=self.description
		)
		theme.save()

		composition = Composition(
			name=self.name,
			slug=self.slug,
			melodies=[melody],
			artists=self.artists,
			theme=theme,
			themes=[theme],
			created=self.created,
			software=software,
			description=self.description
		)

		composition.save()

		song = Song(
			name=self.name,
			artists=self.artists,
			composition=composition,
			compositions=[composition],
			description=self.description
		)

		song.save()

		track = Track(
			name=self.version,
			song=song,
			isrc=self.isrc,
			url='http://example.com'
		)

		track.save()
