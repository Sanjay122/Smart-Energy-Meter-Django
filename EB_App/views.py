from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from . import models

# Create your views here.
from .models import Account


def get_user_role(request):
    username = str(request.user)
    role = "AnonymousUser"
    if username != "AnonymousUser":
        user = User.objects.get(username=username)
        try:
            account = models.Account.objects.filter(user=user).values('role')[0]
            role = account['role']
        except:
            role = "AnonymousUser"
    return role


class LoginView(auth_views.LoginView):
    template_name = "login.html"


class LogoutView(auth_views.LogoutView):
    next_page = "home"


def redirect_login_successful(request):
    user_role = get_user_role(request)
    if user_role == "ADMIN":
        return redirect("adminHome")
    elif user_role == "CONSUMER":
        return redirect("consumerHome")
    return redirect('login')


def get_home(request):
    user_role = get_user_role(request)
    if user_role == "AnonymousUser":
        return render(request=request, template_name="base.html")
    else:
        return redirect("loginSuccessful")


def admin(request):
    user_role = get_user_role(request)
    if user_role == "ADMIN":
        return render(request=request, template_name="admin/home.html")
    return redirect('/login')


def consumer(request):
    user_role = get_user_role(request)
    if user_role == "CONSUMER":
        return render(request=request, template_name="consumer/home.html")
    return redirect('/login')


def get_consumers(request):
    user_role = get_user_role(request)
    if user_role == "ADMIN":
        consumers = []
        users_queryset = models.Account.objects.all().filter(role="CONSUMER").values('user')
        for user in users_queryset:
            user_id = user['user']
            consumers.append(User.objects.get(pk=user_id))
        context = {'consumers': consumers,
                   'consumers_tab_active': 'w3-blue'}
        return render(request=request, template_name="admin/consumers.html", context=context)
    return redirect('/login')
