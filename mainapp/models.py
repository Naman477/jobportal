from django.db import models

# Create your models here.
class LoginInfo(models.Model):
    #id=models.BigAutoField(auto_created=True,primary_key=True)
    usertype = models.CharField(max_length=15)
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=256)
class JobSeeker(models.Model):
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=6)
    contactno=models.CharField(max_length=15)
    emailaddress=models.CharField(max_length=50,primary_key=True)
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=20)
    keyskill=models.CharField(max_length=500)
    address=models.CharField(max_length=500) 
class Enquiry(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    contactno=models.CharField(max_length=12)
    emailaddress=models.EmailField(max_length=50)
    enquirytext=models.TextField()
    posteddate=models.CharField(max_length=30)