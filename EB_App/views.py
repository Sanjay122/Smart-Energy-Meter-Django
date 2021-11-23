from django.shortcuts import redirect, render

from . import helper

# Create your views here.



def getHome(request):
    return render(request=request,template_name="base.html")

def admin(request):    
    user_role=helper.getUserRole(request) 
    if user_role =="ADMIN":
            return render(request=request,template_name="admin_Home.html")        
    return redirect('/login')

def consumer(request):    
    user_role=helper.getUserRole(request) 
    if user_role =="CONSUMER":
            return render(request=request,template_name="consumer_Home.html")        
    return redirect('/login')