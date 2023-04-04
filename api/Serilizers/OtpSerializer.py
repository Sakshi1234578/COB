from ..databaseModels.OTP import OTP
from rest_framework import serializers


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'
