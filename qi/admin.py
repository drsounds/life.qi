from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum, Avg
from qi.models import *
# Register your models here.

class TotalAveragesChangeList(ChangeList):
    #from http://azamatpsw.blogspot.se/2012/01/django-adding-row-to-admin-list-with.html
    #provide the list of fields that we need to calculate averages and totals
    fields_to_total = ['amount',]
 
 
 
    def get_total_values(self, queryset):
        """
        Get the totals
        """
        #basically the total parameter is an empty instance of the given model
        total =  Qi()
        total.custom_alias_name = "Totals" #the label for the totals row
        for field in self.fields_to_total:
            setattr(total, field, queryset.aggregate(Sum(field)).items()[0][1])
        return total
 
 
    def get_average_values(self, queryset):
        """
        Get the averages
        """
        average = Qi()
        average.custom_alias_name = "Averages" #the label for the averages row
 
        for field in self.fields_to_total:
            setattr(average, field, queryset.aggregate(Avg(field)).items()[0][1])
        return average
 
 
    def get_results(self, request):
        """
        The model admin gets queryset results from this method
        and then displays it in the template
        """
        super(TotalAveragesChangeList, self).get_results(request)
        #first get the totals from the current changelist
        total = self.get_total_values(self.query_set)
        #then get the averages
        average = self.get_average_values(self.query_set)
        #small hack. in order to get the objects loaded we need to call for 
        #queryset results once so simple len function does it
        len(self.result_list)
        #and finally we add our custom rows to the resulting changelist
        self.result_list._result_cache.append(total)
        self.result_list._result_cache.append(average)

class QiAdmin(admin.ModelAdmin):
    list_filter = ('account', 'time', 'tags')
    list_display = ('time', 'text', 'account', 'user_disp', 'amount_disp')
    ordering = ('-time',)

class TransactionAdmin(admin.ModelAdmin):
    list_filter = ('time',)
    list_display = ('time', 'amount')
    ordering = ('-time',)

admin.site.register(Qi, QiAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account)
admin.site.register(Currency)
admin.site.register(Tag)

