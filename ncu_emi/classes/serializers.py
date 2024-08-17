from .models import Class
from rest_framework import serializers

class ClassSerializer(serializers.ModelSerializer):
     class Meta:
         model = Class
         fields = ['class_id','class_name','class_path','vector_store_id','user_user']
         read_only_fields = ['class_id']