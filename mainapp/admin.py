from django.contrib import admin
from .models import LoginInfo, JobSeeker, Enquiry


# Register your models here.
admin.site.register(LoginInfo)
admin.site.register(JobSeeker)
admin.site.register(Enquiry)