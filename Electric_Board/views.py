from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from EB_App import models,helper
from django.contrib.auth.views import LoginView

# Create your views here.

def redirectLoginSuccessful(request):
    user_role=helper.getUserRole(request)      
    if user_role=="ADMIN":
        return redirect("EB_App:adminHome")
    elif user_role=="CONSUMER":
        return redirect("EB_App:consumerHome")
    return redirect('/login')