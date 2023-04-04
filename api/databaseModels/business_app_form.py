from django.db import models


class BusinessAppForm(models.Model):
    id = models.AutoField(primary_key=True)
    merchant_business_name = models.CharField(max_length=255, null=True, db_column='merchant_business_name')
    merchant_legal_name = models.CharField(max_length=255, null=True, db_column='merchant_legal_name')
    merchant_address = models.CharField(max_length=255, null=True, db_column='merchant_address')
    product_name = models.CharField(max_length=500, null=True, db_column='product_name')
    types_of_entity = models.CharField(max_length=255, null=True, db_column='types_of_entity')
    year_of_establishment = models.IntegerField(max_length=255, null=True, db_column='year_of_establishment')
    merchant_portal = models.CharField(max_length=255, null=True, db_column='merchant_portal')
    average_transaction_amount = models.CharField(max_length=255,null=True, db_column='average_transaction_amount')
    expected_transactions_numbers = models.CharField(max_length=255,null=True, db_column='expected_transactions_numbers')
    annual_transaction_value = models.CharField(max_length=255, null=True, db_column='annual_transaction_value')
    account_details = models.CharField(max_length=255, null=True, db_column='account_details')
    question = models.IntegerField(null=True, db_column='question')
    authorized_contact_person_name = models.CharField(max_length=255, null=True,
                                                      db_column='authorized_contact_person_name')
    authorized_contact_person_email_id = models.CharField(max_length=255, null=True,
                                                          db_column='authorized_contact_person_email_id')
    authorized_contact_person_contact_number = models.CharField(max_length= 255, null=True,
                                                                   db_column='authorized_contact_person_contact_number')
    technical_contact_person_name = models.CharField(max_length=255, null=True,
                                                     db_column='technical_contact_person_name')
    technical_contact_person_email_id = models.CharField(max_length=255, null=True, db_column='technical_contact_person_email_id')
    technical_contact_person_contact_number = models.CharField( max_length= 255, null=True,
                                                                  db_column='technical_contact_person_contact_number')
    mcc = models.CharField(max_length=255, null=True, db_column='mcc')
    nature_of_business = models.CharField(max_length=255, null=True, db_column='nature_of_business')
    zone = models.CharField(max_length=255, null=True, db_column='zone')
    entity_pan_card_number = models.CharField(max_length=255,null=True, db_column='entity_pan_card_number')
    gst_number = models.CharField(max_length=255,null=True, db_column='gst_number')
    created_on = models.DateTimeField(null=False, blank=False, auto_now_add=True)

    class Meta:
        db_table = "business_app_form"
