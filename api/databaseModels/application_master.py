from django.db import models

class application_master(models.Model): 
    application_id = models.AutoField(primary_key=True)
    application_code = models.CharField(max_length=10, null=True)
    active = models.BooleanField(default=False)
    application_description = models.TextField(null=True)
    ep_url = models.CharField(max_length=255, null=True)
    application_name  = models.CharField(max_length=255, null=True)
    application_url =  models.CharField(max_length=255, null=True)
    class Meta:
        db_table = 'application_master'
