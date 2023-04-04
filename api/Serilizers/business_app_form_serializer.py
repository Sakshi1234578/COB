from rest_framework import serializers
from api.databaseModels.business_app_form import BusinessAppForm
from django.core.exceptions import ValidationError
from ..utils.CodeConstent import codeConstant
import re
from api.utils.custom_exceptions import InvalidDataException
from rest_framework import status

class BusinessAppFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessAppForm
        fields = '__all__'

    def validate(self, data):

        if not re.fullmatch(codeConstant.regex.value, data['authorized_contact_person_email_id']):
            raise InvalidDataException('authorized_contact_person_email_id' , status_code= status.HTTP_400_BAD_REQUEST)

        if len(str(data['authorized_contact_person_contact_number']))!= 10:
            raise InvalidDataException('authorized_contact_person_contact_number is wrong' , status_code= status.HTTP_400_BAD_REQUEST)

        if not re.fullmatch(codeConstant.regex.value, data['technical_contact_person_email_id']):
            raise InvalidDataException('technical_contact_person_email_id is wrong' , status_code= status.HTTP_400_BAD_REQUEST)

        if len(str(data['technical_contact_person_contact_number']))!= 10:
            raise InvalidDataException('technical_contact_person_contact_number is wrong' , status_code= status.HTTP_400_BAD_REQUEST)

        return data