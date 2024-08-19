from .models import Ppt
from rest_framework import serializers

class PptSerializer(serializers.ModelSerializer):
     class Meta:
         model = Ppt
         fields = ['ppt_id','ppt_name','ppt_path','ppt_local_path','class_class']
         read_only_fields = ['ppt_id']