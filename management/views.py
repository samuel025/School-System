from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from management.EmailBackend import EmailBackEnd
# Create your views here.
def HomePage(request):
    return render(request, 'index.html')

def ShowLoginPage(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))
        if user!=None:
            login(request, user)
            if user.user_type=='1':
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=='2':
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid Login Credentials")
            return HttpResponseRedirect('/')

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("logged")
    else:
        return HttpResponse("login")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


