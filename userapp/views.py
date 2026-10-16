from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control
from mainapp.models import JobSeeker,LoginInfo
from adminapp.models import JobInfo
from . models import Response,AppliedJob
import datetime
# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userdash(request):
    try:
        if request.session['userid']!=None:

            js=JobSeeker.objects.get(emailaddress=request.session['userid'])
            jobcount=JobInfo.objects.all().count()
            ajcount=AppliedJob.objects.filter(emailaddress=js.emailaddress).count()
            return render(request,"userdash.html",locals())
    except KeyError:
        messages.error(request,"First do login!!!")
        return redirect ('login') 
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userlogout(request):
    try:
        if request.session['userid']!=None:
            del request.session['userid']
            messages.success(request,"Logged Out Successfully")
            return redirect('login')
    except KeyError:
            messages.error(request,"First do login!!!")
            return redirect('login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def viewjobs(request):
    try:
        if request.session['userid']!=None:
            js=JobSeeker.objects.get(emailaddress=request.session['userid'])
            ji=JobInfo.objects.all()
            return render(request,"viewjobs.html",{"js":js,"ji":ji})
    except KeyError:
        messages.error(request,"First do login!!!")
        return redirect ('login') 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def changeuserpwd(request):
        try:
                if request.session['userid']!=None:
                        if request.method=="POST":
                                oldpassword=request.POST.get("oldpassword")
                                newpassword=request.POST.get("newpassword")
                                confirmpassword=request.POST.get("confirmpassword")
                                if newpassword!=confirmpassword:
                                        messages.error(request,"Newpassword and Confirmpassword are not equal")
                                        return redirect("changeuserpwd")
                                try:
                                        obj=LoginInfo.objects.get(username=request.session['userid'], password=oldpassword)
                                        LoginInfo.objects.filter(username=request.session['userid']).update(password=newpassword)
                                        messages.success(request,"Password is changed successfully")
                                        return redirect("userlogout")
                                except:
                                        messages.error(request,"Old password is not matched")
                                        return redirect("changeuserpwd")
                        return render(request,"changeuserpwd.html")
        except KeyError:
                messages.error(request,"Please login first!")
                return redirect('login') 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def giveresponse(request):
    try:
        if request.session['userid']!=None:
            js=JobSeeker.objects.get(emailaddress=request.session['userid'])
            if request.method=="POST":
                responsetype=request.POST.get("responsetype")
                subject=request.POST.get("subject")
                responsetext=request.POST.get("responsetext")
                name=js.name
                contactno=js.contactno
                posteddate=datetime.datetime.today().strftime("%d/%m/%y")
                res=Response(name=name,contactno=contactno,responsetype=responsetype,subject=subject,responsetext=responsetext,posteddate=posteddate)
                res.save()
                messages.success(request,"your response is submitted successfully" )
                return redirect("giveresponse")
            return render(request,"giveresponse.html",{"js":js})
    except KeyError:
        messages.error(request,"First do login!!!")
        return redirect ('login')            
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def applyjob(request,jobid):
    try:
        if request.session['userid']!=None:
            js=JobSeeker.objects.get(emailaddress=request.session['userid'])
            check_applied=AppliedJob.objects.filter(jobid=jobid,emailaddress=js.emailaddress).exists()
            if check_applied:
                messages.warning(request,"you have already applied for this job")
                return redirect("viewjobs")
            job=JobInfo.objects.get(id=jobid)
            jobid=job.id
            title=job.title
            description=job.description
            name=js.name
            contactno=js.contactno
            emailaddress=js.emailaddress
            qualification=js.qualification
            experience=js.experience
            keyskill=js.keyskill
            applieddate=datetime.datetime.today().strftime("%d/%m/%Y")
            aj=AppliedJob(jobid=jobid,title=title,description=description,name=name,contactno=contactno,emailaddress=emailaddress,qualification=qualification,experience=experience,keyskill=keyskill,applieddate=applieddate)
            aj.save()
            messages.success(request,"you have applied job successfully")
            return redirect('viewjobs')
    except KeyError:
        messages.error(request,"First do login!!!")
        return redirect ('login')                                
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def userprofile(request):
    try:
        if request.session['userid']!=None:
            js=JobSeeker.objects.get(emailaddress=request.session['userid'])
            return render(request,"userprofile.html",locals())
    except KeyError:
        messages.error(request,"First do login!!!")
        return redirect ('login') 
