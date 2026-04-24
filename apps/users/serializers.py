from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'user_name',
            'user_document',
            'user_address',
            'user_email',
            'user_phone_number',
        ]
