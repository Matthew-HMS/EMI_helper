from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'read_only': True},
            'user_pw': {'write_only': True},
            'is_active':{'default':0},
        }

    def create(self, validated_data):
        validated_data['user_pw'] = make_password(validated_data['user_pw'])
        return super(UserSerializer, self).create(validated_data)

class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['user_account', 'user_pw']
        extra_kwargs = {
            'user_pw': {'write_only': True}
        }