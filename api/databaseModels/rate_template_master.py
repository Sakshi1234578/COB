from django.db import models


class RateTemplateMaster(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    rate_template_code = models.CharField(max_length=100, null=True, db_column='rate_template_code')
    rate_template_name = models.CharField(max_length=200, null=True, db_column='rate_template_name')
    client_code = models.CharField(max_length=100, null=True, db_column='client_code')
    business_cat_code = models.CharField(max_length=100, null=True, db_column='business_cat_code')
    risk_cat_code = models.CharField(max_length=100, null=True, db_column='risk_cat_code')
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'rate_template_master'
