from ..databaseModels.lookup_category import lookup_category
from rest_framework import serializers


class lookup_category_serializer(serializers.ModelSerializer):
    class Meta:
        model = lookup_category
        fields = '__all__'
