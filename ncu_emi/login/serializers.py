from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password, check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id','user_account', 'user_pw', 'user_name','is_active','last_login']
        read_only_fields = ['user_id']
        extra_kwargs = {
            'user_pw': {'write_only': True}  
        }

class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['user_account', 'user_pw']
        extra_kwargs = {
            'user_pw': {'write_only': True}
        }