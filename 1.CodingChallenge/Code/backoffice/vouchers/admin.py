from django.contrib import admin

from vouchers.models import InteractionLog, Voucher

# Register your models here.
admin.site.register(Voucher)
admin.site.register(InteractionLog)