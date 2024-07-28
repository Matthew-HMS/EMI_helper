from .models import Class
from rest_framework import serializers

class classSerializer(serializers.ModelSerializer):
     class Meta:
         model = Class
         fields = ['class_name','user_user']