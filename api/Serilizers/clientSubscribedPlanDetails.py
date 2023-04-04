from ..databaseModels.client_subscribed_plan_details import client_subscribed_plan_details
from rest_framework import serializers


class clientSubscribedPlanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = client_subscribed_plan_details
        fields = '__all__'
