from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            redirect("/recruiter-dashboard")
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'app/index.html', context)

    context = {}
    return render(request, 'app/index.html', context)

def logout_user(request):
    logout(request)
    return redirect('home/')

def signup_candidate(request):
    return render(request, 'app/signup_candidate.html')

def signup_recruiter(request):
    return render(request, 'app/signup_recruiter.html')

def dashboard_recruiter(request):
    skills = ['html', 'python', 'css']
    return render(request, 'app/recruiter_dashboard.html', {'jobTitle': 'worker', 'jobSource': 'google', 'jobDesc': 'know how to code', 'skills': skills})
