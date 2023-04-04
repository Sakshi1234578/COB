from django.db import models


class client_account_details(models.Model):
    clinet_account_id = models.AutoField(primary_key=True)
    account_holder_name = models.CharField(max_length=255, null=True)
    account_number = models.CharField(max_length=255, null=True)
    ifsc_code = models.CharField(max_length=255, null=True)
    merchantId = models.IntegerField(null=True)
    bankId = models.IntegerField(null=True)
    accountType = models.CharField(max_length=100, null=True)
    branch = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'client_account_details'
