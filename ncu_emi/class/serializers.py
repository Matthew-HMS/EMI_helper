from .models import Class
from rest_framework import serializers

class classSerializer(serializers.ModelSerializer):
     class Meta:
         model = Class
         fields = ['class_id','class_name','user_user']
         read_only_fields = ['class_id']