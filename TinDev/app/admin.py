from django.contrib import admin
from app.models import Candidate, Recruiter, Job


admin.site.register(Candidate)
admin.site.register(Recruiter)
admin.site.register(Job)
# Register your models here.
