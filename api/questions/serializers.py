from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ['name', 'n_questions', 'n_attempts']
