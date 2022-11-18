from django.db import models

# Create your models here.
class Candidate(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
    bio = models.TextField(max_length=500)
    skills = models.TextField()
    github = models.CharField(max_length=50)
    yoe = models.IntegerField()
    education = models.CharField(max_length=50)
    
    
class Recruiter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    zip = models.IntegerField()
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
    status = models.CharField(max_length=50) # active or inactive

