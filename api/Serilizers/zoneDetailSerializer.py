from ..databaseModels.zone_master import zone_master
from rest_framework import serializers


class zoneDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = zone_master
        fields = '__all__'
