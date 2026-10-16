from django.db import models



# Create your models here.
class Response(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    contactno=models.CharField(max_length=15)
    responsetype=models.CharField(max_length=50)
    subject=models.CharField(max_length=500)
    responsetext=models.CharField(max_length=2000)
    posteddate=models.CharField(max_length=30)

class  AppliedJob(models.Model):
    id=models.AutoField(primary_key=True)
    jobid=models.IntegerField()
    title=models.TextField()
    description=models.TextField()
    name=models.CharField(max_length=50)
    contactno=models.CharField(max_length=15)
    emailaddress=models.CharField(max_length=50)
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=20)
    keyskill=models.CharField(max_length=500)
    applieddate=models.CharField(max_length=30)