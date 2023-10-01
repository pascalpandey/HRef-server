from django.http import JsonResponse
from .serializers import CandidateSerializer, EmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Candidate, Employee
import requests
import os


def download_and_save_pdf(url):
    response = requests.get(url, stream=True)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Get the filename from the URL
        filename = url.split("/")[-1]

        # Define the local path where you want to save the file
        local_path = os.path.join("path_to_local_directory", filename)

        # Save the file locally
        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)


@api_view(['GET', 'POST'])
def candidate(request):
    if request.method == 'GET':
        queries = Candidate.objects.all()
        serializer = CandidateSerializer(queries, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = CandidateSerializer(data=request.data)

# get employee
@api_view(['GET', 'POST'])
def employee(request):
    if request.method == 'GET':
        queries = Employee.objects.all()
        serializer = EmployeeSerializer(queries, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(status=201) 
        return Response(serializer.errors, status=400) 
