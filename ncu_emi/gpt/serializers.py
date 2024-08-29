from .models import Class
from .models import Pptword
from rest_framework import serializers

class PptWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pptword
        fields = ['pptword_id', 'pptword_page', 'pptword_content', 'ppt_ppt', 'pptword_question']
        read_only_fields = ['pptword_id']