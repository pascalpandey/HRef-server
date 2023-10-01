from django.http import JsonResponse
from .serializers import CandidateSerializer, EmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Candidate, Employee
import requests
import os


def download_and_save_pdf(url):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        filename = url.split("/")[-1]
        base_dir = os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))) 
        pdfs_directory = os.path.join(base_dir, 'pdfs')
        os.makedirs(pdfs_directory, exist_ok=True)
        local_path = os.path.join(pdfs_directory, filename)
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
        for url in request.data['data']:
            download_and_save_pdf(url)
        return Response("Success")


@api_view(['GET', 'POST'])
def employee(request):
    if request.method == 'GET':
        queries = Employee.objects.all()
        serializer = EmployeeSerializer(queries, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
