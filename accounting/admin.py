from django.contrib import admin
from accounting.models import *
# Register your models here.
class Admin(admin.ModelAdmin):
    list_filter = ('account', 'time', 'tags')
    list_display = ('time', 'text', 'account', 'user_disp', 'amount_disp')
    ordering = ('-time',)

class TransactionAdmin(admin.ModelAdmin):
    list_filter = ('time', 'text',)
    list_display = ('time', 'text', 'amount',)
    ordering = ('-time',)

class VoucherAdmin(admin.ModelAdmin):
    list_display = ('time', 'title', 'text')
    ordering = ('-time',)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account)
admin.site.register(Currency)
admin.site.register(Tag)
admin.site.register(Voucher, VoucherAdmin)

