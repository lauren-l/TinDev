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
from .models import Candidate, Recruiter, Job
from django.db import connection

# Create your views here.
def home(request):

    if request.method == 'POST':
        l_username = request.POST.get('username')
        l_password = request.POST.get('password')

        recruiter = Recruiter.objects.filter(username=l_username, password=l_password)
        candidate = Candidate.objects.filter(username=l_username, password=l_password)

        if recruiter:
            request.session['username'] = l_username
            return redirect("/recruiter_dashboard")
        elif candidate:
            request.session['username'] = l_username
            return redirect("/candidate_dashboard")
        else:
            # messages.info(request, 'Username or password is incorrect')
            messages.add_message(request, messages.INFO, 'Username or password is incorrect')
            return render(request, 'app/index.html')

    return render(request, 'app/index.html')

def logout_user(request):
    request.session.flush()
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

def dashboard_candidate(request):
    jobData = list(Job.objects.values("title", "company", "description", "skills", "city", "state", "job_type", "expiration"))
    for item in jobData:
        item["skills"] = list(item["skills"].split(","))
    return render(request, 'app/candidate_dashboard.html', {"jobs": jobData})

def dashboard_recruiter(request):
    context = {}

    # set default post fitlers
    context["myPosts"] = False
    context["active"] = True
    context["inactive"] = False
    context["numCandidates"] = 0
    context["myPostsCheckedStatus"] = "unchecked"
    context["activeCheckedStatus"] = "checked"
    context["inactiveCheckedStatus"] = "unchecked"

    if request.method == 'POST':
        context["myPosts"] = False if request.POST.get('my-post') == None else True
        context["active"] = False if request.POST.get('post-status-active') == None else True
        context["inactive"] = False if request.POST.get('post-status-inactive') == None else True
        context["numCandidates"] = request.POST.get('candidateRange')
    
    if context["active"] and not context["inactive"]: # only active posts
        data = list(Job.objects.filter(
            active=True,
            numCandidates__gte = context["numCandidates"]
        ).values("title", "company", "description", "skills", "city", "state", "coverImage", "active", "job_type", "numCandidates"))
    elif context["inactive"] and not context["active"]: # only inactive posts
        data = list(Job.objects.filter(
            active=False,
            numCandidates__gte = context["numCandidates"]
        ).values("title", "company", "description", "skills", "city", "state", "coverImage", "active", "job_type", "numCandidates"))
    elif context["active"] and context["inactive"]:
        data = list(Job.objects.filter(
            numCandidates__gte = context["numCandidates"]
        ).values("title", "company", "description", "skills", "city", "state", "coverImage", "active", "job_type", "numCandidates"))
    else:
        data = []

        

    for item in data:
        item["numCandidates"] = str(item["numCandidates"])
        item["coverImage"] = item["coverImage"].replace("app/static/", "")
        item["skills"] = list(item["skills"].split(","))
        item["status"] = "Active" if item["active"] else "Inactive"
    
    context["jobs"] = data
    context["activeCheckedStatus"] = "checked" if context["active"] else "unchecked"
    context["inactiveCheckedStatus"] = "checked" if context["inactive"] else "unchecked"
    context["myPostsCheckedStatus"] = "checked" if context["myPosts"] else "unchecked"



    return render(request, 'app/recruiter_dashboard.html', context=context)

def candidate_offers(request):
    jobData = list(Job.objects.values("title", "company", "description", "skills", "city", "state", "job_type", "expiration"))
    for item in jobData:
        item["skills"] = list(item["skills"].split(","))

    # Need to check for specific account
    # candData = list(Candidate.objects.values("first_name, last_name, skills, github"))
    # for item in candData:
    #     item["skills"] = list(item["skills"].split(","))

    return render(request, 'app/candidate_offers.html', {"jobs": jobData})
