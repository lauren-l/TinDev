from django.contrib import admin
from app.models import Candidate, Recruiter, Job, Offers, Applications


admin.site.register(Candidate)
admin.site.register(Recruiter)
admin.site.register(Job)
admin.site.register(Offers)
admin.site.register(Applications)
# Register your models here.
