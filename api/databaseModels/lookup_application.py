from django.db import models


class lookup_application(models.Model):
    applicationId = models.AutoField(primary_key=True, db_column='application_id')
    applicationname = models.CharField(max_length=50, null=True, db_column='application_name')

    class Meta:
        db_table = 'lookup_application'
