from django.contrib import admin
from drsounds.models import *

class ReleaseTrackInline(admin.StackedInline):
    model = ReleaseTrack
    ordering = ('number',)


class SongAdmin(admin.ModelAdmin):
    pass


admin.site.register(Song, SongAdmin)


class QuickTrackAdmin(admin.ModelAdmin):
    pass


admin.site.register(QuickTrack, QuickTrackAdmin)


class UniverseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Universe, UniverseAdmin)


class DimensionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Dimension, DimensionAdmin)


class VideoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Video, VideoAdmin)


class ServiceAdmin(admin.ModelAdmin):
    pass


admin.site.register(Service, ServiceAdmin)


class ServiceReleaseAdmin(admin.ModelAdmin):
    pass


admin.site.register(ServiceRelease, ServiceReleaseAdmin)



class ReleaseAdmin(admin.ModelAdmin):
    inlines = [
        ReleaseTrackInline
    ]
    pass


admin.site.register(Release, ReleaseAdmin)


class LabelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Label, LabelAdmin)




class AssemblyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Assembly, AssemblyAdmin)


class MelodyStyleAdmin(admin.ModelAdmin):
	pass

admin.site.register(MelodyStyle, MelodyStyleAdmin)





class ArtistAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artist, ArtistAdmin)


class CompositionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Composition, CompositionAdmin)

class MelodyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Melody, MelodyAdmin)



class TrackAdmin(admin.ModelAdmin):
    pass

admin.site.register(Track, TrackAdmin)


class ComposerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Composer, ComposerAdmin)


class MixAdmin(admin.ModelAdmin):
    pass


admin.site.register(Mix, MixAdmin)


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genre, GenreAdmin)


class ThemeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Theme, ThemeAdmin)



class EpisodeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Episode, EpisodeAdmin)



class ShowAdmin(admin.ModelAdmin):
    pass


admin.site.register(Show, ShowAdmin)



class ChannelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Channel, ChannelAdmin)
