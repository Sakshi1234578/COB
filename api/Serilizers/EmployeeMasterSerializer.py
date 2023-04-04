from ..databaseModels.employee_master import employee_master
from rest_framework import serializers


class employeeMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee_master
        fields = '__all__'
