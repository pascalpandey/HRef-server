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
    
# accept employee
@api_view(['POST'])
def acceptCandidate(request, id):
    try:
        candidate = Candidate.objects.get(id=id)
        
        Employee.objects.create(
            id=candidate.id,
            keywords=candidate.keywords,
            color=candidate.color,
            resume_link=candidate.resume_link,
            score=candidate.score,
            x=candidate.x,
            y=candidate.y
        )
        
        candidate.delete()

        # retrain model here!

        return Response({"message": "Candidate accepted and moved to employee table."}, status=201)
    
    except Candidate.DoesNotExist:
        return Response({"message": "Candidate not found."}, status=404)

# reject employee
@api_view(['DELETE'])
def rejectCandidate(request, id):
    try:
        candidate = Candidate.objects.get(id=id)
        candidate.delete()
        
        # retrain model here!

        return Response({"message": "Candidate rejected successfully"}, status=200)
    
    except Candidate.DoesNotExist:
        return Response({"message": "Candidate not found."}, status=404)


