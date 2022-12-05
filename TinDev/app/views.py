from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import RSignUpForm, CSignUpForm
from .models import *
from django.db import connection

# CONSTANTS
SKILL_CHOICES = (
    ("1", "Python"),
    ("2", "Tableau"),
    ("3", "SQL"),
    ("4", "Java"),
    ("5", "C++"),
    ("6", "C"),
    ("7", "Go"),
    ("8", "PHP"),
    ("9", "R"),
    ("10", "Swift"),
    ("11", "HTML"),
    ("12", "CSS"),
    ("13", "JavaScript"),
    ("14", "AWS"),
    ("15", "Bash"),
    ("16", "Perl"),
    ("17", "Azure"),
    ("18", "React.js"),
    ("19", "MySQL"),
    ("20", "Machine Learning"),
    ("21", "Vue.js"),
    ("22", "C#"),
    ("23", "Natual Language Processing"),
    ("24", "Docker")
)
# Create your views here.
def home(request):
    if request.method == 'POST':
        l_username = request.POST.get('username')
        l_password = request.POST.get('password')

        recruiter = Recruiter.objects.filter(username=l_username, password=l_password)
        candidate = Candidate.objects.filter(username=l_username, password=l_password)

        if recruiter:
            request.session['uid'] = recruiter[0].id
            print(request.session['uid'])
            return redirect("/recruiter_dashboard")
        elif candidate:
            request.session['uid'] = candidate[0].id
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
            b1.save()

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
            b1.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/home')
            
    else:
        form = RSignUpForm()
        
    return render(request, 'app/signup_recruiter.html', {'form': form})

# this function demonstrates candate interest & calculates compatibility score upon button click
def submit_application(request):
    if request.method == 'GET':
        candidate_id = int(request.session['uid'])
        job_id = request.GET['jid']

        # checking if already applied
        if Applications.objects.filter(job_id=job_id, candidate_id=candidate_id):
            return HttpResponse("Already applied")
        
        # haven't applied yet
        job = Job.objects.filter(id=job_id)[0]
        job_description = job.description
        recruiter_id = job.author
        num_candidates = job.numCandidates
        candidate = Candidate.objects.filter(id=candidate_id)[0]
        skills = candidate.skills.split(",")
        yoe = candidate.yoe

        # updating num candidates of job
        job.numCandidates = job.numCandidates + 1
        job.save()

        # calculating compatibility score
        # skill overlap: 50%
        # experience: 50%
            # (yoe) / (num_candidates + yoe)
            # more candidates => higher yoe => higher compatibility
            # less candidates => lower yoe => higher compatibility
        # calculations:
            # evaluate skill_overlap and experience to be out of 100, then take the average of the 2
            # resulting compatibility score should also be out of 100

        skill_overlap = max(30, (len(skills) / len(SKILL_CHOICES)) * 100)
        experience = max(30, (yoe / (num_candidates + yoe)) * 100)
        cscore = (skill_overlap + experience) // 2
        
        application = Applications.objects.create(job_id=job_id, candidate_id=request.session['uid'], compatibility_score=cscore)
        return HttpResponse("Success")
    
    else: 
        return HttpResponse("Request method is not a GET")



def dashboard_candidate(request):
    context = {}
    # set default post fitlers
    context["myPost"] = False
    context["active"] = True
    context["inactive"] = False
    context["partTime"] = True
    context["fullTime"] = True
    context["locSF"] = False
    context["locNY"] = False
    context["locAu"] = False
    context["myPostsCheckedStatus"] = "unchecked"
    context["activeCheckedStatus"] = "checked"
    context["inactiveCheckedStatus"] = "unchecked"
    context["partTimeCheckedStatus"] = "checked"
    context["fullTimeCheckedStatus"] = "checked"
    context["SFCheckedStatus"] = "checked"
    context["NYCheckedStatus"] = "checked"
    context["AuCheckedStatus"] = "checked"
    
    if request.method == 'GET':
        jobData = list(Job.objects.filter(
            active=True
        ).values("title", "company", "description", "skills", "city", "state", "job_type", "expiration", "id"))
        for item in jobData:
            item["skills"] = list(item["skills"].split(","))
        context["jobs"] = jobData
        return render(request, 'app/candidate_dashboard.html', context)
    
    elif request.method == 'POST':
        keywords = set(request.POST.get('post_search_keyword').lower().split())
        jobData = list(Job.objects.values("title", "company", "description", "skills", "city", "state", "job_type", "expiration", "id"))
        jobs = list(filter(lambda x: not keywords.isdisjoint(set(x['description'].lower().split())), jobData))
        for item in jobs:
            item["skills"] = list(item["skills"].split(","))
        context["job"] = jobData
        return render(request, 'app/candidate_dashboard.html', context)



def dashboard_recruiter(request):
    context = {}
    recruiter_id = request.session['uid']
    print(recruiter_id)

    # set default post fitlers
    context["myPosts"] = False
    context["active"] = True
    context["inactive"] = False
    context["numCandidates"] = 0
    context["myPostsCheckedStatus"] = "unchecked"
    context["activeCheckedStatus"] = "checked"
    context["inactiveCheckedStatus"] = "unchecked"

    if request.method == 'POST':
        # if user wants to view applicant for certain job
        if request.POST.get("view-applicants"):
            # redirect to view applicant portal w/ job id
            request.session['job-id'] = request.POST.get("view-applicants")
            return redirect(f'/view_applicants')
        context["myPosts"] = False if request.POST.get('my-post') == None else True
        context["active"] = False if request.POST.get('post-status-active') == None else True
        context["inactive"] = False if request.POST.get('post-status-inactive') == None else True
        context["numCandidates"] = request.POST.get('candidateRange')
    
    if context["active"] and not context["inactive"]: # only active posts
        data = list(Job.objects.filter(
            active=True,
            numCandidates__gte = context["numCandidates"]
        ).values("id", "title", "company", "description", "skills", "city", "state", "coverImage", "active", "job_type", "numCandidates", "author"))
    elif context["inactive"] and not context["active"]: # only inactive posts
        data = list(Job.objects.filter(
            active=False,
            numCandidates__gte = context["numCandidates"]
        ).values("id", "title", "company", "description", "skills", "city", "state", "coverImage", "active", "job_type", "numCandidates", "author"))
    elif context["active"] and context["inactive"]:
        data = list(Job.objects.filter(
            numCandidates__gte = context["numCandidates"]
        ).values("id", "title", "company", "description", "skills", "city", "state", "coverImage", "active", "job_type", "numCandidates", "author"))
    else:
        data = []

    # filtering data to only include jobs of current user/recruiter
    if context["myPosts"]:
        data = list(filter(lambda x: str(x['author']) == str(recruiter_id), data))
    
    for item in data:
        item["numCandidates"] = str(item["numCandidates"])
        item["coverImage"] = item["coverImage"].replace("app/static/", "")
        item["skills"] = list(item["skills"].split(","))
        item["status"] = "Active" if item["active"] else "Inactive"
        # only enable view applicants button if user is the author of the post
        item["viewApplicants"] = "disabled" if str(item['author']) == str(recruiter_id) else ""
    
    
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

def view_applicants(request):
    jobId = request.session["job-id"]
    # get all applications with matching job-id
    applications = list(Applications.objects.filter(job_id = jobId, recruiter_id = request.session['uid']).values("candidate_id", "compatibility_score"))

    # get and parse data for all candidates who submitted an application
    for applicant in applications:
        applicant_info = list(Candidate.objects.filter(id = applicant["candidate_id"]).values("first_name", "last_name", "bio", "yoe", "education", "github", "zip", "skills"))
        applicant["first_name"] = applicant_info[0]["first_name"]
        applicant["last_name"] = applicant_info[0]["last_name"]
        applicant["bio"] = applicant_info[0]["bio"]
        applicant["yoe"] = applicant_info[0]["yoe"]
        applicant["education"] = applicant_info[0]["education"]
        applicant["github"] = applicant_info[0]["github"]
        applicant["zip"] = applicant_info[0]["zip"]
        applicant["skills"] = applicant_info[0]["skills"].split(",")


    # render page with all applicants for job
    return render(request, 'app/view_applicants.html', {"applicants": applications})