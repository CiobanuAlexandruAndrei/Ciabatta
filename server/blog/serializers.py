from rest_framework import serializers
from .models import *


class KeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keyword
        fields = ['name']
