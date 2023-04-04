from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.login_master)
admin.site.register(models.bank_master)
admin.site.register(models.client_account_details)
admin.site.register(models.client_super_master)
admin.site.register(models.lookup_role)
admin.site.register(models.lookup_state)
admin.site.register(models.merchant_data)
admin.site.register(models.TempKyc)
admin.site.register(models.client_application_mapper)
admin.site.register(models.lookup_application)
admin.site.register(models.merchant_document)
admin.site.register(models.OTP)
admin.site.register(models.Verification)