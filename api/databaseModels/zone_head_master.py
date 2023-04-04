from django.db import models


class zone_head_master(models.Model):
    id = models.AutoField(primary_key=True)
    zoneCode = models.CharField(
        max_length=45, null=True, db_column='zone_code')
    zoneHeadName = models.CharField(
        max_length=45, null=True, db_column='zone_head_name')
    empCode = models.CharField(
        max_length=45, null=True, db_column='emp_code')
    isActive = models.BooleanField(default=True, 
        db_column='is_active')
    class Meta:
        db_table = 'zone_head_master'