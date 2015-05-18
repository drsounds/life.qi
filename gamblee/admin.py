from django.contrib import admin
from gamblee.models import *
# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    pass

class CompanyAdmin(admin.ModelAdmin):
    pass

class PlayAdmin(admin.ModelAdmin):
    list_display = ('time', 'game', 'cost', 'prize',)
    order = ('-time',)
    pass

class GameAdmin(admin.ModelAdmin):
    pass

admin.site.register(Game, GameAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Play, PlayAdmin)
admin.site.register(Account, AccountAdmin)