from rest_framework import serializers
from ..databaseModels.rate_template_master import RateTemplateMaster


class RateTemplateMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateTemplateMaster
        fields = ['rate_template_code', 'rate_template_name', 'client_code']
