from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def getCandidates(request):
    # query the db here
    return HttpResponse("This is the candidates list view.")
