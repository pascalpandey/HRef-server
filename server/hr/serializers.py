from rest_framework import serializers
from .models import Query, Output


class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['query']


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = ['output']
