from rest_framework import serializers
from .models import *


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['name']

class KeywordClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordCluster
        fields = '__all__'

class APICostRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = APICostRecord
        fields = ['id', 'cost', 'timestamp']