from django.db import models

# Create your models here.
class JobInfo(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.TextField()
    description=models.TextField()
    location=models.TextField()
    salary=models.IntegerField()
    jobtype=models.CharField(max_length=50)
    lastdate=models.CharField(max_length=30)
    posteddate=models.CharField(max_length=30)