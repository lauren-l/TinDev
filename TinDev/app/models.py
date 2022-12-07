'''
this file contains models for objects: Candidate, Recruiter, Job, Applications, and Offers
'''
from django.db import models
from django.core.validators import MinLengthValidator
from django.forms import ModelForm

# candidate model
class Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    zip = models.CharField(max_length=5, validators=[
            MinLengthValidator(5, 'the field must contain at least 5 characters')
            ])
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, default='N/A')
    skills = models.TextField()
    github = models.CharField(max_length=50, default='None')
    yoe = models.IntegerField()
    education = models.CharField(max_length=50, default="N/A")
    interested = models.CharField(max_length=500, default="")
    disinterested = models.CharField(max_length=500, default="")
    
    
class Recruiter(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    zip = models.CharField(max_length=5, validators=[
            MinLengthValidator(5, 'the field must contain at least 5 characters')
            ])
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Job(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=30)
    skills = models.TextField()
    description = models.TextField()
    company = models.CharField(max_length=50)
    expiration = models.DateTimeField()
    active = models.BooleanField()
    author = models.CharField(max_length=50)
    numCandidates = models.IntegerField()
    coverImage = models.ImageField(upload_to ='app/static/images', default='../../static/images/errorImage.jpg')

class Applications(models.Model):
    job_id = models.CharField(max_length=50)
    candidate_id = models.CharField(max_length=50)
    recruiter_id = models.CharField(max_length=50)
    compatibility_score = models.FloatField()

class Offers(models.Model):
    job_id = models.CharField(max_length=50)
    candidate_id = models.CharField(max_length=50)
    recruiter_id = models.CharField(max_length=50)
    offerDeadline = models.DateTimeField()
    salary = models.FloatField()
    response = models.BooleanField()
    accepted = models.BooleanField()

class UpdatePosts(ModelForm):
    class Meta:
        model = Job
        fields = ['author', 'title', 'job_type', 'city', 'state', 'skills', 'description', 'active']