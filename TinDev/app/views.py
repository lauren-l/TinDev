from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import RSignUpForm, CSignUpForm, OfferForm, CreatePosts, UpdatePosts
from .models import *
from django.db import connection

# CONSTANTS (compatibility score dependency)
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

def home(request):
    if request.method == 'POST':
        l_username = request.POST.get('username')
        l_password = request.POST.get('password')

        recruiter = Recruiter.objects.filter(username=l_username, password=l_password)
        candidate = Candidate.objects.filter(username=l_username, password=l_password)

        # storing user information for current session
        if recruiter:
            request.session['uid'] = recruiter[0].id
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
            return HttpResponseRedirect('/home') # redirect to home (sign in)
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
            return HttpResponseRedirect('/home') # redirect to home (sign in)
    else:
        form = RSignUpForm()
    return render(request, 'app/signup_recruiter.html', {'form': form})

# this function demonstrates candidate interest & calculates compatibility score upon button click
def submit_application(request):
    if request.method == 'GET':
        candidate_id = int(request.session['uid'])
        job_id = request.GET['jid']

        # checking if already applied
        if Applications.objects.filter(job_id=job_id, candidate_id=candidate_id):
            return HttpResponse("Already applied")
        
        # if haven't applied yet
        # prepare to calculate cscore & submit application
        job = Job.objects.filter(id=job_id)[0]
        job_description = job.description
        recruiter_id = job.author
        num_candidates = job.numCandidates
        candidate = Candidate.objects.filter(id=candidate_id)[0]
        skills = candidate.skills.split(",")
        yoe = candidate.yoe

        # update num candidates of job
        job.numCandidates = job.numCandidates + 1
        job.save()

        # calculating compatibility score
        '''
        skill overlap: 50%
        experience: 50%
            # (yoe) / (num_candidates + yoe)
            # more candidates => higher yoe => higher compatibility
            # less candidates => lower yoe => higher compatibility
        calculations:
            # evaluate skill_overlap and experience to be out of 100, then take the average of the 2
            # resulting compatibility score should also be out of 100
        '''
        skill_overlap = max(30, (len(skills) / len(SKILL_CHOICES)) * 100)
        experience = max(30, (yoe / (num_candidates + yoe)) * 100)
        cscore = (skill_overlap + experience) // 2
        
        # create application object
        application = Applications.objects.create(job_id=job_id, candidate_id=request.session['uid'], compatibility_score=cscore)
        application.save()
        return HttpResponse("Success")
    
    else: 
        return HttpResponse("Request method is not a GET")

def dashboard_candidate(request):
    context = {}
    candidate_id = request.session['uid']
    keywords = None

    # set default post filters
    context["first_name"] = False
    context["last_name"] = False
    context["myPosts"] = False
    context["interested"] = False
    context["uninterested"] = False
    context["active"] = True
    context["inactive"] = False
    context["numCandidates"] = 0
    context["interestedCheckedStatus"] = "unchecked"
    context["myPostsCheckedStatus"] = "unchecked"
    context["activeCheckedStatus"] = "checked"
    context["inactiveCheckedStatus"] = "unchecked"

    # if using searchbar or post filters
    if request.method == 'POST':
        keywords = request.POST.get('post_search_keyword') # check if any search keywords
        # filter criteria
        context["interested"] = False if request.POST.get('post-status-interested') == None else True
        context["uninterested"] = False if request.POST.get('post-status-uninterested') == None else True
        context["myPosts"] = False if request.POST.get('my-post') == None else True
        context["active"] = False if request.POST.get('post-status-active') == None else True
        context["inactive"] = False if request.POST.get('post-status-inactive') == None else True
        context["numCandidates"] = request.POST.get('candidateRange')

    if keywords: # if using search bar and NOT filter function
        keywords = set(keywords.lower().split())
        jobData = list(Job.objects.values("id", "title", "company", "description", "skills", "city", "state", "coverImage", "active", "job_type", "numCandidates", "author"))
        data = list(filter(lambda x: not keywords.isdisjoint(set(x['description'].lower().split())), jobData)) # filter out jobs that don't have keyword(s) in job description
            
    # filter functionality starts here
    elif context["interested"] and not context["uninterested"]: # only interested posts
        data = list(Job.objects.filter(
            active=True,
            numCandidates__gte = context["numCandidates"]
        ).values("id", "title", "company", "description", "skills", "city", "state", "coverImage", "active", "job_type", "numCandidates", "author"))
    elif context["active"] and not context["inactive"]: # only active posts
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

    # filtering data to only include jobs of current user
    if context["myPosts"]:
        data = list(filter(lambda x: str(x['author']) == str(candidate_id), data))
    
    for item in data:
        item["numCandidates"] = str(item["numCandidates"])
        item["coverImage"] = item["coverImage"].replace("app/static/", "")
        item["skills"] = list(item["skills"].split(","))
        item["status"] = "Active" if item["active"] else "Inactive"
     
    context["jobs"] = data

    cand_info = list(Candidate.objects.filter(id = candidate_id).values("first_name", "last_name", "skills", "profilePicture"))[0]
    context["first_name"] = cand_info["first_name"]
    context["last_name"] = cand_info["last_name"]
    context["skills"] = list(cand_info["skills"].split(","))
    context["profilePicture"] = cand_info["profilePicture"].replace("app/static/", "")

    return render(request, 'app/candidate_dashboard.html', context=context)

def dashboard_recruiter(request):
    context = {}
    recruiter_id = request.session['uid']

    # set default post fitlers
    context["myPosts"] = False
    context["active"] = True
    context["inactive"] = False
    context["numCandidates"] = 0

    # checked status = status of checkbox
    context["myPostsCheckedStatus"] = "unchecked"
    context["activeCheckedStatus"] = "checked"
    context["inactiveCheckedStatus"] = "unchecked"

    if request.method == 'POST':
        # if user wants to view applicant for certain job
        if request.POST.get("view-applicants"):
            # redirect to view applicant portal w/ job id
            request.session['job-id'] = request.POST.get("view-applicants")
            return redirect(f'/view_applicants')
        else:
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
    elif context["active"] and context["inactive"]: # both active and inactive posts
        data = list(Job.objects.filter(
            numCandidates__gte = context["numCandidates"]
        ).values("id", "title", "company", "description", "skills", "city", "state", "coverImage", "active", "job_type", "numCandidates", "author"))
    else: # no posts (neither active nor inactive)
        data = []

    # filtering data to only include jobs of current user/recruiter
    if context["myPosts"]:
        data = list(filter(lambda x: str(x['author']) == str(recruiter_id), data))
    
    for item in data: # clean job info in context
        item["numCandidates"] = str(item["numCandidates"])
        item["coverImage"] = item["coverImage"].replace("app/static/", "")
        item["skills"] = list(item["skills"].split(","))
        item["status"] = "Active" if item["active"] else "Inactive"
        # disable view applicants button if user is not the author of the post
        item["viewApplicants"] = "disabled" if str(item['author']) != str(recruiter_id) else ""
        item["editMyPost"] = "hidden" if str(item['author']) != str(recruiter_id) else ""
    
    context["jobs"] = data
    context["activeCheckedStatus"] = "checked" if context["active"] else "unchecked"
    context["inactiveCheckedStatus"] = "checked" if context["inactive"] else "unchecked"
    context["myPostsCheckedStatus"] = "checked" if context["myPosts"] else "unchecked"
    

    # prevents user from editing or deleting other recruiters' job posts

    return render(request, 'app/recruiter_dashboard.html', context=context)

def candidate_offers(request):
    context = {}
    candidate_id = request.session['uid']
    print(candidate_id)

    # get all offers with matching candidate id
    offers = list(Offers.objects.filter(id = candidate_id).values("job_id", "candidate_id", "recruiter_id", "offerDeadline", "salary", "response", "accepted"))
    # date__range=["2022-12-01", offers[i]['offerDeadline']]

    # get job info from offers
    for i, offer in enumerate(offers):
        offer_info = list(Job.objects.filter(id = offers[i]['job_id']).values("title", "job_type", "city", "state", "company", "expiration", "active", "author", "coverImage"))[0]
        offer["title"] = offer_info["title"]
        offer["job_type"] = offer_info["job_type"]
        offer["city"] = offer_info["city"]
        offer["state"] = offer_info["state"]
        offer["company"] = offer_info["company"]
        offer["expiration"] = offer_info["expiration"]
        offer["active"] = offer_info["active"]
        offer["author"] = offer_info["author"]
        offer["coverImage"] = offer_info["coverImage"].replace("app/static/", "")
    
    print(offers)
    for i, offer in enumerate(offers):
        if offer["offerDeadline"] < timezone.now():
            offers.pop(i)
            # offer["offerDeadline"] = 'Deadline Passed!'

    context["offers"] = offers

    return render(request, 'app/candidate_offers.html', context=context)

def offer_response(request):
    if request.method == 'GET':
        c_id = request.session['uid']
        job_id = request.GET['jid']
        
        offer = Offers.objects.get(id=job_id, candidate_id=c_id)
        if offer.response == True: 
            return HttpResponse("Already responded")
        else:
            if (request.POST.get('acc') == True):
                offer.accepted = True
            else: offer.accepted = False
            offer.response = True
        offer.save()
        
    #         if request.method == 'GET':
    #     candidate_id = int(request.session['uid'])
    #     job_id = request.GET['jid']
        
    # accepted = request.POST.get['offer-status-accept']

    # offer = Offers.objects.get(id=job_id, candidate_id=candidate_id)
    # if offer:
    #     if offer.response == True: 
    #         return HttpResponse("Already responded")
    #     else:
    #         offer.response = True
    #         if accepted: offer.accepted = True
    #         else: offer.accepted = False
    #     offer.save()
        
        return HttpResponse("Success")

def view_applicants(request):
    form = OfferForm()
    jobId = request.session["job-id"]
    # get all applications with matching job-id
    applications = list(Applications.objects.filter(job_id = jobId, recruiter_id = request.session['uid']).values("candidate_id", "compatibility_score"))

    if request.method == 'POST':
        # if an offer was sent
        form = OfferForm(request.POST)

        # get applicant id (id of candidate)
        applicant_id = request.POST.get("applicant-id")

        # get the salary + expiration date entered
        if form.is_valid():
            Nsalary = form.cleaned_data['salary']
            expiration = form.cleaned_data["expirationDate"]

        # query database for offer w/ matching details (candidate -> job)
        existingOffer = Offers.objects.get(job_id=jobId, candidate_id=applicant_id)
        
        if existingOffer:
            # if an offer exists for the job for the applicant, update the entry
            existingOffer.salary=Nsalary
            existingOffer.offerDeadline= expiration
            existingOffer.save()
        else: # if no preexisting offer, create new offer
            b1 = Offers.objects.create(job_id=jobId, candidate_id=applicant_id, recruiter_id=request.session["uid"],offerDeadline=expiration, salary=Nsalary, response=False, accepted=False)
            b1.save()
            
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
    return render(request, 'app/view_applicants.html', {"applicants": applications,"form":form})

def create_posts(request):
    if request.method == 'POST':
        form = CreatePosts(request.POST)    # takes form from the CreatePosts class in forms.py
        if form.is_valid():

            # Convert the select all input that are integers to match with skills values
            skills = ""
            for count, skill in enumerate(form.cleaned_data['skills']):
                skills = skills+SKILL_CHOICES[int(skill)][1]                
                if count != len(form.cleaned_data['skills'])-1:
                    skills = skills + ", "

            # create objects based on user input and save
            b1 = Job.objects.create(author=request.session['uid'], title=form.cleaned_data['title'], job_type=form.cleaned_data['job_type'], city=form.cleaned_data['city'], state=form.cleaned_data['state'], skills=skills, description=form.cleaned_data['description'], company=form.cleaned_data['company'], expiration=form.cleaned_data['expiration'], active=form.cleaned_data['active'], numCandidates=0)
            b1.save()

            # redirect to dashboard again
            return HttpResponseRedirect('/recruiter_dashboard')
            
    else:
        form = CreatePosts()
        
    return render(request, 'app/create_posts.html', {'form': form})

def update_posts(request, pk):
    # model = Job
    # template = 'update_posts.html'
    # fields = ['author', 'title', 'job_type', 'city', 'state', 'skills', 'description', 'active']

    if request.method == 'POST':
        job_post=Job.objects.get(pk=pk)
        form = UpdatePosts(request.POST, instance=job_post)
        if form.is_valid():
            # update the post
            form.save()
            # redirect to same update page URL:
            return HttpResponseRedirect('/update_posts/'+str(pk))
            
    else:
        job_post=Job.objects.get(pk=pk)
        form = UpdatePosts(instance=job_post)
        return render(request, 'app/update_posts.html', {'form': form})  
        

def delete_posts(request, pk):
    Job.objects.filter(pk=pk).delete()
    return HttpResponseRedirect('/recruiter_dashboard')

