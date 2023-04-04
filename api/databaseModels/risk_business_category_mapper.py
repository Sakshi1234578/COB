from django.db import models


class risk_business_category_mapper(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    risk_category = models.CharField(max_length=100, null=True, db_column='risk_category')
    business_category_id = models.CharField(max_length=100, null=True, db_column='business_category_id')

    class Meta:
        db_table = 'risk_business_category_mapper'
