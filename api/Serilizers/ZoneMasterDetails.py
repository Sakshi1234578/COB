from ..databaseModels.zone_head_master import zone_head_master
from rest_framework import serializers


class zoneMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = zone_head_master
        fields = '__all__'
