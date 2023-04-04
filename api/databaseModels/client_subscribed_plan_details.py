from django.db import models
import datetime
from datetime import timedelta
import uuid
def get_mendate_end_time():
    return datetime.datetime.today() + timedelta(days=30)

class client_subscribed_plan_details(models.Model):
    clientSubscribedPlanDetailsId = models.AutoField(primary_key=True, db_column='client_subscribed_plan_id')
    clientId = models.CharField(max_length=10, null=True, db_column='client_id')
    clientCode = models.CharField(max_length=5, null=True, db_column='client_code')
    clientName = models.CharField(max_length=255, null=True, db_column='client_name')
    applicationId= models.IntegerField(null=True, db_column='application_id')
    applicationName = models.CharField(max_length=100, null=True, db_column='application_name')
    planId= models.IntegerField(null=True, db_column='plan_id')
    planName = models.CharField(max_length=100, null=True, db_column='plan_name')
    purchaseAmount = models.DecimalField(null=True, db_column='purchase_amount', max_digits=10, decimal_places = 3)
    mandateRegistrationId =  models.CharField(max_length=50, null=True, db_column='mandate_registration_id', default=uuid.uuid4())
    umrn = models.CharField(max_length=50, null=True)
    paymentMode = models.CharField(max_length=20, null=True, db_column='payment_mode')
    bankRef = models.CharField(max_length=50, null=True, db_column='bank_ref_no')
    mandateStatus = models.CharField(max_length=10, null=True, db_column='mandate_status')
    clientTxnId = models.CharField(max_length=50, null=True, db_column='client_txn_id')
    mandateTime = models.DateTimeField(null=True, db_column='mandate_time')
    mandateStartTime=models.DateTimeField(auto_now_add=True, db_column='mandate_start_time')
    mandateEndTime = models.DateTimeField(default=get_mendate_end_time, db_column='mandate_end_time')
    mandateBankName = models.CharField(max_length=20, null=True, db_column='mandate_bank_name')
    mandateFrequency = models.CharField(max_length=20,null=True, db_column='mandate_frequency')

    class Meta:
        db_table = 'client_subscribed_plan_details'
