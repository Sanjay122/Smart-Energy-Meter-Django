from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Account)
admin.site.register(models.Consumer)
admin.site.register(models.MonthWiseData)
admin.site.register(models.WeekWiseData)
admin.site.register(models.DayWiseData)
admin.site.register(models.WithinADayData)
admin.site.register(models.Bill)