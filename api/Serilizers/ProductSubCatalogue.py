from ..databaseModels.application_sub_plan_master import application_sub_plan_master
from rest_framework import serializers


class product_subdetails_serializer(serializers.ModelSerializer):
    class Meta:
        model = application_sub_plan_master
        fields = '__all__'