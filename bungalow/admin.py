from django.contrib import admin
from bungalow.models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    pass

class OutcomeAdmin(admin.ModelAdmin):
    pass

class StatusCodeAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class InqueryInline(admin.StackedInline):
    model = Inquery
    ordering = ('-time',)

class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'added', 'updated', 'user', 'category', 'outcome', 'status',)
    list_filter = ('category', 'status', 'outcome',)
    ordering = ('priority', '-added',)
    inlines = [InqueryInline,]
    pass

class InqueryAdmin(admin.ModelAdmin):
    ordering = ('-time',)
    pass

admin.site.register(Opportunity, OpportunityAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(StatusCode, StatusCodeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Outcome, OutcomeAdmin)



