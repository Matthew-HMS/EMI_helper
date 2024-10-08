from .models import Prompt
from rest_framework import serializers

class PromptSerializer(serializers.ModelSerializer):
     class Meta:
         model = Prompt
         fields = ['prompt_id','prompt_name','prompt_content','user_user']
         read_only_fields = ['prompt_id']