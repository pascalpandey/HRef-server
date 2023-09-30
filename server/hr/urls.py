from django.urls import path
from . import views

urlpatterns = [
    path('', views.getCandidates, name='candidates_list'),
    # Add more URL patterns for your "candidates" app here
]
