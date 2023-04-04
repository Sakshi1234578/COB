from api.Serilizers import business_app_form_serializer
from api.databaseModels.business_app_form import BusinessAppForm
from rest_framework.response import Response
from datetime import datetime,timedelta
from api.utils.data import ModifyPage

def business_app_form_data(form_data):
    business_form_serializer = business_app_form_serializer.BusinessAppFormSerializer(data=form_data)
    if business_form_serializer.is_valid(raise_exception=True):
        business_form_serializer.save()
        return True

def get_data(start_date,end_date): 
    get_business_form = BusinessAppForm.objects.filter(created_on__range=(start_date,end_date + timedelta(days=1)))
    print(get_business_form.query)
    return business_app_form_serializer.BusinessAppFormSerializer(get_business_form, many=True).data  


def complete_data():
    obj=BusinessAppForm.objects.all()
    serializer_class = business_app_form_serializer.BusinessAppFormSerializer
    pagination_class= ModifyPage
    return business_app_form_serializer.BusinessAppFormSerializer(obj, many=True).data
