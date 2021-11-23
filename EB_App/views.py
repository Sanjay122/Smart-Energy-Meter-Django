from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import AnonymousUser, User, auth

from django.contrib.auth.views import LoginView

# Create your views here.

def getUser(request):
    user=None
    if request.user.is_authenticated():
        user= request.user
    return user

def getHome(request):
    return render(request=request,template_name="base.html")

def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/adminHome')
    else:
        return LoginView()

def logout(request):
    auth.logout(request)
    return redirect('/')

def admin(request):    
    username=request.user
    if str(username) !="AnonymousUser":
            return render(request=request,template_name="home.html")        
    return redirect('/login')