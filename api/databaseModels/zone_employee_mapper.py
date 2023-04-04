from django.db import models


class zone_employee_mapper(models.Model):
    id = models.AutoField(primary_key=True, db_column='state_id')
    zoneCode = models.CharField(
        max_length=45, null=True, db_column='zone_code')
    empCode = models.CharField(
        max_length=45, null=True, db_column='emp_code') 
    class Meta:
        db_table = 'zone_employee_mapper'

