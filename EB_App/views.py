from django.shortcuts import render

# Create your views here.

def getHome(request):
    return render(request=request,template_name="base.html")