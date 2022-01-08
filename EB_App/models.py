# importing date class from datetime module
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)
    role = models.CharField(max_length=120)
    authorities = models.CharField(max_length=120)
    isEnabled = models.BooleanField()

    def __str__(self):
        return self.user.username + '  ' + self.role


class Consumer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    supply_phase = models.IntegerField()
    door_number = models.CharField(max_length=120, null=True, blank=True)
    street = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    post_office = models.CharField(max_length=120)
    taluk = models.CharField(max_length=120)
    district = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    pin_number = models.IntegerField()
    eb_number = models.CharField(max_length=14)

    def __str__(self):
        return self.account.user.username


class Message(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.TextField()


class Bill(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    last_bill_reading = models.FloatField()
    present_bill_reading = models.FloatField()
    power_consumption = models.FloatField()
    bill_amount = models.FloatField()
    paid = models.BooleanField()


class MonthWiseData(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    power_consumed = models.FloatField()
    average_voltage = models.FloatField()
    average_current = models.FloatField()
    average_power_factor = models.FloatField()


class WeekWiseData(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
    power_consumed = models.FloatField()
    average_voltage = models.FloatField()
    average_current = models.FloatField()
    average_power_factor = models.FloatField()


class DayWiseData(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
    day = models.IntegerField()
    power_consumed = models.FloatField()
    average_voltage = models.FloatField()
    average_current = models.FloatField()
    average_power_factor = models.FloatField()


class WithinADayData(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    power_consumed = models.FloatField()
    average_voltage = models.FloatField()
    average_current = models.FloatField()
    average_power_factor = models.FloatField()

    def get_absolute_url(self):
        return reverse("home")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        last_bill = Bill.objects.filter(consumer=self.consumer).last()
        if last_bill is not None:
            last_bill_reading = last_bill.present_bill_reading
        else:
            last_bill_reading = 0
        units_consumed = self.power_consumed - last_bill_reading
        if 80 < units_consumed % 100 < 100:
            message = Message(account=self.consumer.account,
                              message=str(units_consumed) + " units have been consumed on " + str(today))
            message.save()
        if self.average_power_factor < 0.7:
            message = Message(account=Account.objects.get(id=1),
                              message="Power factor is " + str(self.average_power_factor) + ", add Capacitive bank")
            message.save()
        if today.hour < 1:
            if DayWiseData.objects.filter(consumer=self.consumer,
                                          year=yesterday.year,
                                          month=yesterday.month,
                                          day=yesterday.day) is None:
                within_a_day_data = WithinADayData.objects.filter(consumer=self.consumer,
                                                                  year=yesterday.year,
                                                                  month=yesterday.month,
                                                                  day=yesterday.day)
                if within_a_day_data is not None:
                    average_voltage = 0
                    average_current = 0
                    average_power_factor = 0
                    power_consumed = 0
                    for obj in within_a_day_data:
                        average_voltage += obj.average_voltage
                        average_current += obj.average_current
                        average_power_factor += obj.average_power_factor
                        power_consumed = obj.power_consumed
                    average_voltage /= len(within_a_day_data)
                    average_current /= len(within_a_day_data)
                    average_power_factor /= len(within_a_day_data)
                    day_wise_data = DayWiseData(consumer=self.consumer, year=yesterday.year,
                                                month=yesterday.month,
                                                week=yesterday.isocalendar()[1],
                                                day=yesterday.day,
                                                power_consumed=power_consumed,
                                                average_voltage=average_voltage,
                                                average_current=average_current,
                                                average_power_factor=average_power_factor)
                    day_wise_data.save()
                    # WeekWiseData
                    if today.isocalendar()[1] != yesterday.isocalendar()[1]:
                        if WeekWiseData.objects.filter(consumer=self.consumer,
                                                       year=yesterday.year,
                                                       month=yesterday.month,
                                                       week=yesterday.isocalendar()[1]) is None:
                            day_wise_data = DayWiseData.objects.filter(consumer=self.consumer,
                                                                       year=yesterday.year,
                                                                       month=yesterday.month,
                                                                       week=yesterday.isocalendar()[1])
                            if day_wise_data is not None:
                                average_voltage = 0
                                average_current = 0
                                average_power_factor = 0
                                power_consumed = 0
                                for obj in day_wise_data:
                                    average_voltage += obj.average_voltage
                                    average_current += obj.average_current
                                    average_power_factor += obj.average_power_factor
                                    power_consumed = obj.power_consumed
                                average_voltage /= len(day_wise_data)
                                average_current /= len(day_wise_data)
                                average_power_factor /= len(day_wise_data)
                                week_wise_data = WeekWiseData(consumer=self.consumer,
                                                              year=yesterday.year,
                                                              month=yesterday.month,
                                                              week=yesterday.isocalendar()[1],
                                                              power_consumed=power_consumed,
                                                              average_voltage=average_voltage,
                                                              average_current=average_current,
                                                              average_power_factor=average_power_factor)
                                week_wise_data.save()
                    if today.month != yesterday.month:
                        if MonthWiseData.objects.filter(consumer=self.consumer,
                                                        year=yesterday.year,
                                                        month=yesterday.month) is None:
                            week_wise_data = WeekWiseData.objects.filter(consumer=self.consumer,
                                                                         year=yesterday.year,
                                                                         month=yesterday.month)
                            if week_wise_data is not None:
                                average_voltage = 0
                                average_current = 0
                                average_power_factor = 0
                                power_consumed = 0
                                units_consumed = 0
                                for obj in week_wise_data:
                                    average_voltage += obj.average_voltage
                                    average_current += obj.average_current
                                    average_power_factor += obj.average_power_factor
                                    power_consumed = obj.power_consumed
                                average_voltage /= len(week_wise_data)
                                average_current /= len(week_wise_data)
                                average_power_factor /= len(week_wise_data)
                                month_wise_data = MonthWiseData(consumer=self.consumer,
                                                                year=yesterday.year,
                                                                month=yesterday.month,
                                                                power_consumed=power_consumed,
                                                                average_voltage=average_voltage,
                                                                average_current=average_current,
                                                                average_power_factor=average_power_factor)
                                month_wise_data.save()
                                last_bill = Bill.objects.filter(consumer=self.consumer).last()
                                if last_bill is not None:
                                    last_bill_reading = last_bill.present_bill_reading
                                else:
                                    last_bill_reading = 0
                                units_consumed = power_consumed - last_bill_reading
                                price = 0
                                if units_consumed <= 100:

                                    price = 0

                                elif units_consumed <= 200:

                                    price = ((100 * 0) +
                                             (units_consumed - 100) * 1.5) + 20

                                elif units_consumed <= 500:

                                    price = ((100 * 0) +
                                             (100 * 2) +
                                             (units_consumed - 200) * 3) + 30

                                elif units_consumed > 500:

                                    price = ((100 * 0) +
                                             (100 * 3.5) +
                                             (300 * 4.6) +
                                             (units_consumed - 500) * 6.6) + 50

                                bill = Bill(consumer_id=1,
                                            year=yesterday.year,
                                            month=yesterday.month,
                                            last_bill_reading=last_bill_reading,
                                            present_bill_reading=power_consumed,
                                            power_consumption=units_consumed,
                                            bill_amount=price,
                                            paid=False)
                                bill.save()
                                previous_1_month_date = today.replace(day=1) - timedelta(days=1)
                                previous_2_month_date = previous_1_month_date.replace(day=1) - timedelta(days=1)
                                try:
                                    WithinADayData.objects.get(consumer=self.consumer, year=previous_2_month_date.year,
                                                               month=previous_2_month_date.month).delete()
                                    DayWiseData.objects.get(consumer=self.consumer, year=previous_2_month_date.year,
                                                            month=previous_2_month_date.month).delete()
                                    WeekWiseData.objects.get(consumer=self.consumer, year=previous_2_month_date.year,
                                                             month=previous_2_month_date.month).delete()
                                    Message.objects.get(consumer=self.consumer, year=previous_2_month_date.year,
                                                        month=previous_2_month_date.month).delete()
                                except:
                                    print("Error in deleting 2nd month data")
