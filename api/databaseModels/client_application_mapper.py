from django.db import models


class client_application_mapper(models.Model):
    client_application_mapper_id = models.AutoField(primary_key=True)
    clientId = models.ForeignKey('api.client_super_master', on_delete=models.CASCADE, null=True, db_column='client_id')
    application_id = models.ForeignKey('api.lookup_application', on_delete=models.CASCADE, null=True, db_column='application_id')
    createdDate = models.DateTimeField(auto_now_add=True, db_column='created_date')
    responseDate = models.DateTimeField(auto_now_add=True, db_column='response_date')
    status = models.CharField(max_length=50, null=True)
    reason = models.CharField(max_length=255, null=True)
    configurationStatus = models.CharField(max_length=50, null=True, db_column='configuration_status')
    subscriptionStatus = models.CharField(max_length=45, null=True, db_column='subscription_status')
    createdBy = models.IntegerField(null=True, db_column='created_by')
    modifiedBy = models.IntegerField(null=True, db_column='modified_by')
    modifiedDate = models.DateTimeField(auto_now=True, db_column='modified_date')

    class Meta:
        db_table = 'client_application_mapper'
