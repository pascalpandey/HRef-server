from rest_framework import serializers
from .models import Candidate, Employee

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'keywords', 'color', 'resume_link', 'score', 'x', 'y']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'keywords', 'color', 'resume_link', 'score', 'x', 'y']

