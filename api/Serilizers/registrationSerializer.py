from rest_framework import serializers
import re
from ..databaseModels.login_master import login_master
from ..utils.CodeConstent import codeConstant
from api.databaseModels.website_app_plan_detail import WebsiteAppPlanDetail


class registration_loginserializer(serializers.ModelSerializer):
    class Meta:
        model = login_master
        fields = '__all__'

    def validate(self, data):
        if data['email'] == '':
            raise serializers.ValidationError(
                codeConstant.email_required.value)
        elif not re.fullmatch(codeConstant.regex.value, data['email']):
            raise serializers.ValidationError(
                codeConstant.Email_not_valid.value)
        if data['mobileNumber'] == '':
            raise serializers.ValidationError(
                codeConstant.Mobile_number_required.value)
        elif len(data['mobileNumber']) != 10:
            raise serializers.ValidationError(codeConstant.Mobile_error.value)
        if data['name'] == '':
            raise serializers.ValidationError(codeConstant.Name_required.value)
        if data['password'] == '':
            raise serializers.ValidationError(
                codeConstant.Password_required.value)
        if data['business_cat_code'] == '':
            raise serializers.ValidationError(
                codeConstant.Business_category.value)

        return data


class website_login_serializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteAppPlanDetail
        fields = '__all__'
