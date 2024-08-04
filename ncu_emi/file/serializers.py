from .models import File
from rest_framework import serializers

class fileSerializer(serializers.ModelSerializer):
     class Meta:
         model = File
         fields = ['file_id','file_name','file_path','class_class']
         read_only_fields = ['file_id']