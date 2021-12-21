# importing date class from datetime module
from datetime import datetime

from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import generic

from . import models, forms

# Create your views here.

active_tab = 'w3-blue'


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
        context = {'overview_tab_active': active_tab}
        return render(request=request, template_name="consumer/home.html", context=context)
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
                   'consumers_tab_active': active_tab}
        return render(request=request, template_name="admin/consumers.html", context=context)
    return redirect('/login')


class WithinADayDataCreateView(generic.CreateView):
    extra_context = {'overview_tab_active': active_tab}
    template_name = 'consumer/WithinADayDataCreate.html'
    form_class = forms.WithinADayDataModelForm


def reset_consumption_table(request):
    user_role = get_user_role(request)
    if user_role == "ADMIN":
        models.WithinADayData.objects.all().delete()
        models.DayWiseData.objects.all().delete()
        models.WeekWiseData.objects.all().delete()
        models.MonthWiseData.objects.all().delete()
        models.Bill.objects.all().delete()
        return redirect("adminHome")
    return redirect('/login')


def get_day_wise_data(consumer_obj, date):
    day_wise_data = models.DayWiseData.objects.filter(consumer=consumer_obj, year=date.year, month=date.month,
                                                      day=date.day)
    data = []
    if day_wise_data is not None:
        for obj in day_wise_data:
            data.append(obj)
    return data


def get_within_a_day_wise_data(consumer_obj, date):
    within_a_day_wise_data = models.WithinADayData.objects.filter(consumer=consumer_obj, year=date.year,
                                                                  month=date.month, day=date.day)
    data = []
    if within_a_day_wise_data is not None:
        for obj in within_a_day_wise_data:
            data.append(obj)
    return data


def get_user(username):
    user = None
    user_obj = User.objects.filter(username=username)
    for obj in user_obj:
        user = obj
    if user is None:
        return "AnonymousUser"
    account = models.Account.objects.get(user=user)
    if account.role == "CONSUMER":
        return models.Consumer.objects.get(account=account)
    elif account.role == "ADMIN":
        return account


def get_consumer_day_wise_data(request):
    user = get_user(username=str(request.user))
    if user != "AnonymousUser":
        if user.account.role == "CONSUMER":
            context = {'within_a_day_wise_data': get_within_a_day_wise_data(user, date=datetime.now()),
                       'live_data_tab_active': active_tab}
            return render(request=request, template_name="consumer/live_data.html", context=context)
    return redirect('/login')
