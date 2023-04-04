from django.db import models


class lookup_category(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    category_name = models.CharField(
        max_length=200, null=True, db_column='category_name')
    category_code = models.CharField(
        max_length=200, null=True, db_column='category_code')
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'lookup_category'
