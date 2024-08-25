from .models import Ppt
from .models import Ppt_page
from rest_framework import serializers

class PptSerializer(serializers.ModelSerializer):
     class Meta:
         model = Ppt
         fields = ['ppt_id','ppt_name','ppt_path','ppt_local_path','class_class']
         read_only_fields = ['ppt_id']

class Ppt_pageSerializer(serializers.ModelSerializer):
     class Meta:
         model = Ppt_page
         fields = ['ppt_page_id','uploaded_id','ppt_ppt']
         read_only_fields = ['ppt_page_id']

