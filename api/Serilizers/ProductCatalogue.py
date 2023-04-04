from ..databaseModels.application_master import application_master
from rest_framework import serializers


class product_catalogue_serializer(serializers.ModelSerializer):
    class Meta:
        model = application_master
        fields = '__all__'