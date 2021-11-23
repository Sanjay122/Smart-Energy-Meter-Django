from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth

from django.contrib.auth.views import LoginView

# Create your views here.

def redirectLoginSuccessful(request):
    return redirect('EB_App:adminHome')