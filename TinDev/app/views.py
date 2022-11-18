from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import RSignUpForm, CSignUpForm
from .models import Candidate, Recruiter

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
    if request.method == 'POST':
        form = CSignUpForm(request.POST)
        if form.is_valid():
            # create candidate object
            b1 = Candidate.objects.create(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], zip=form.cleaned_data['zip'], username=form.cleaned_data['username'], password=form.cleaned_data['password'], bio=form.cleaned_data['bio'], skills=form.cleaned_data['skills'], github=form.cleaned_data['github'], yoe=form.cleaned_data['yoe'], education=form.cleaned_data['education'])

            # redirect to a new URL:
            return HttpResponseRedirect('/home')
            
    else:
        form = CSignUpForm()
        
    return render(request, 'app/signup_candidate.html', {'form': form})

def signup_recruiter(request):
    if request.method == 'POST':
        form = RSignUpForm(request.POST)
        if form.is_valid():
            # create recruiter object
            b1 = Recruiter.objects.create(first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], company=form.cleaned_data['company'], zip=form.cleaned_data['zip'], username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            # redirect to a new URL:
            return HttpResponseRedirect('/home')
            
    else:
        form = RSignUpForm()
        
    return render(request, 'app/signup_recruiter.html', {'form': form})

def dashboard_recruiter(request):
    skills = ['html', 'python', 'css']
    return render(request, 'app/recruiter_dashboard.html', {'jobTitle': 'worker', 'jobSource': 'google', 'jobDesc': 'know how to code', 'skills': skills})
