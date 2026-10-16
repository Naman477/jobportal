"""
URL configuration for jobportal project.
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from mainapp import views as main_views
from adminapp import views as admin_views
from userapp import views as user_views

urlpatterns = [
    path('ping/', lambda request: HttpResponse('pong', content_type='text/plain'), name='ping'),
    path('admin/', admin.site.urls),

    # --- mainapp routes ---
    path('', main_views.index, name='index'),
    path('about/', main_views.about, name='about'),
    path('contact/', main_views.contact, name='contact'),
    path('login/', main_views.login, name='login'),
    path('register/', main_views.register, name='register'),

    # --- adminapp routes ---
    path('admindash/', admin_views.admindash, name='admindash'),
    path('adminlogout/', admin_views.adminlogout, name='adminlogout'),
    path('jobseeker/', admin_views.jobseeker, name='jobseeker'),
    path('postjob/', admin_views.postjob, name='postjob'),
    path('postedjob/', admin_views.postedjob, name='postedjob'),
    path('enquiries/', admin_views.enquiries, name='enquiries'),
    path('changeadminpwd/', admin_views.changeadminpwd, name='changeadminpwd'),
    path('viewfeedback/', admin_views.viewfeedback, name='viewfeedback'),
    path('viewcomplaint/', admin_views.viewcomplaint, name='viewcomplaint'),
    path('deleteenq/<int:id>/', admin_views.deleteenq, name='deleteenq'),
    path('appliedjob/', admin_views.appliedjob, name='appliedjob'),

    # --- userapp routes ---
    path('userdash/', user_views.userdash, name='userdash'),
    path('userlogout/', user_views.userlogout, name='userlogout'),
    path('viewjobs/', user_views.viewjobs, name='viewjobs'),
    path('changeuserpwd/', user_views.changeuserpwd, name='changeuserpwd'),
    path('giveresponse/', user_views.giveresponse, name='giveresponse'),
    path('applyjob/<int:jobid>/', user_views.applyjob, name='applyjob'),
    path('userprofile/', user_views.userprofile, name='userprofile'),
]
