from django.contrib import admin

from vouchers.models import InteractionLog, Voucher

# Register your models here. para mostrar en el Admmin
admin.site.register(Voucher)
admin.site.register(InteractionLog)