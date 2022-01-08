# importing date class from datetime module
from datetime import datetime

from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import generic
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models, forms, web_connection

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
        context = {'base': active_tab}
        return render(request=request, template_name="base.html",context=context)
    else:
        return redirect("loginSuccessful")


def admin(request):
    user_role = get_user_role(request)
    if user_role == "ADMIN":
        return render(request=request, template_name="admin/home.html")
    return redirect('login')


# def consumer(request):
#     user_role = get_user_role(request)
#     if user_role == "CONSUMER":
#         context = {'overview_tab_active': active_tab}
#         return render(request=request, template_name="consumer/home.html", context=context)
#     return redirect('login')


def consumer(request):
    user = get_user(username=str(request.user))
    if user != "AnonymousUser":
        if user.account.role == "CONSUMER":
            units_consumed = models.WithinADayData.objects.last()  # type: models.WithinADayData
            context = {'overview_tab_active': active_tab,
                       'consumer': user,
                       'last_within_a_day_data': units_consumed}
            return render(request=request, template_name="consumer/home.html", context=context)
    return redirect('login')


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
    return redirect('login')


class WithinADayDataCreateView(generic.CreateView):
    extra_context = {'overview_tab_active': active_tab}
    template_name = 'consumer/WithinADayDataCreate.html'
    form_class = forms.WithinADayDataModelForm


def reset_consumption_table_granted():
    models.WithinADayData.objects.all().delete()
    models.DayWiseData.objects.all().delete()
    models.WeekWiseData.objects.all().delete()
    models.MonthWiseData.objects.all().delete()
    models.Bill.objects.all().delete()
    models.Message.objects.all().delete()


def reset_consumption_table(request):
    user_role = get_user_role(request)
    if user_role == "ADMIN":
        reset_consumption_table_granted()
        return redirect("adminHome")
    return redirect('login')


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
            context = {'within_a_day_wise_data': get_within_a_day_wise_data(user, date=datetime(2021,12,29)),
                       'live_data_tab_active': active_tab}
            return render(request=request, template_name="consumer/live_data.html", context=context)
    return redirect('login')


@api_view()
def get_consumer_day_wise_data_json(request, *args, **kwargs):
    user = get_user(username=str(request.user))
    if user != "AnonymousUser":
        if user.account.role == "CONSUMER":
            values = []
            labels = []
            i = 0
            for obj in get_within_a_day_wise_data(models.Consumer.objects.get(id=user.id), date=datetime(2021,12,29)):
                i += 1
                labels.append(i)
                values.append(float(obj.average_current))
            data = {
                "labels": labels,
                "default": values
            }
            return Response(data)
    return redirect('login')


def get_consumer_data_admin(request, id):
    user = get_user(username=str(request.user))
    if user != "AnonymousUser":
        if user.role == "ADMIN":
            user_obj = User.objects.get(id=id)
            account_obj = models.Account.objects.get(user=user_obj)
            consumer_obj = models.Consumer.objects.get(account=account_obj)
            context = {'consumer': consumer_obj,
                       'consumers_tab_active': active_tab,
                       'last_bill': models.Bill.objects.filter(consumer=consumer_obj).last(),
                       'power_consumed': models.WithinADayData.objects.filter(
                           consumer=consumer_obj).last().power_consumed}
            return render(request=request, template_name="admin/consumer_data.html", context=context)
    return redirect('login')


def generate_random_data(request):
    user = get_user(username=str(request.user))
    if user != "AnonymousUser":
        if user.role == "ADMIN":
            reset_consumption_table_granted()

            web_connection.generate()
            return redirect('adminHome')
    return redirect('login')


def get_bills(consumer_id):
    bills = []
    for obj in models.Bill.objects.filter(consumer_id=consumer_id):
        bills.append(obj)
    return bills


def get_bills_consumer(request):
    user = get_user(username=str(request.user))
    if user != "AnonymousUser":
        if user.account.role == "CONSUMER":
            bills = get_bills(user.id)
            context = {'bill_tab_active': active_tab,
                       'consumer': user,
                       'bills': bills}
            return render(request=request, template_name="consumer/bills.html", context=context)
    return redirect('login')


def unit_rate(request):
    context = {'unit_rate_tab_active': active_tab}
    return render(request=request, template_name='about_bill_calc.html', context=context)
