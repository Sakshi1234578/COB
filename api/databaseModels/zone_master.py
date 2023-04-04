from django.db import models


class zone_master(models.Model):
    id = models.AutoField(primary_key=True)
    zoneCode = models.CharField(
        max_length=10, null=True, db_column='zone_code')
    zoneName = models.CharField(
        max_length=45, null=True, db_column='zone_name')
    zoneManager = models.CharField(
        max_length=45, null=True, db_column='zone_manager')
    isActive = models.BooleanField(default=True, 
        db_column='is_active')
    class Meta:
        db_table = 'zone_master'



 

