from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'index.html')

def signup_candidate(request):
    return render(request, 'app/signup_candidate.html')

def signup_recruiter(request):
    return render(request, 'app/signup_recruiter.html')
