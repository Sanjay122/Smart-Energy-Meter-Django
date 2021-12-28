"""Electric_Board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_home, name="home"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('', include('django.contrib.auth.urls')),
    path("accounts/profile/", views.redirect_login_successful, name="loginSuccessful"),
    path('adminHome/', views.admin, name="adminHome"),
    path('admin/consumers/', views.get_consumers, name="consumers"),
    path('consumerHome/', views.consumer, name="consumerHome"),
    path('insertWithinADayDataCreate/', views.WithinADayDataCreateView.as_view(), name="insertWithinADayDataCreate"),
    path('reset_consumption_table/', views.reset_consumption_table, name="deleteConsumptionRecord"),
    path('consumer_live_data/', views.get_consumer_day_wise_data, name="consumerLiveData"),
    path('consumer_live_data_api/', views.get_consumer_day_wise_data_json, name="consumerLiveDataApi"),
    path('admin/consumer_data/<int:id>/', views.get_consumer_data_admin, name="consumerDataAdmin"),
    path('admin/generate_random_data/', views.generate_random_data, name="generateRandomData"),
]
