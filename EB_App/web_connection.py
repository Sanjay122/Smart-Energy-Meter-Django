# importing date class from datetime module
import random
from datetime import datetime, timedelta

from . import models


def generate():
    today = datetime.now()
    this_month = today.replace(day=1)
    last_month = this_month - timedelta(days=1)
    date_pointer = last_month.replace(day=1)
    previous_pointer = None
    last_message_sent_pf = None
    last_message_sent_consumption = None
    voltage_max = 245
    voltage_min = 240
    current_max = .5
    current_min = .1
    power_factor_max = .85
    power_factor_min = .55
    power_consumed_range_min = .005
    power_consumed_range_max = .05
    power_consumed = 0
    power_consumed_total = 0
    while date_pointer < today:
        hour = 0
        # WithinADay data
        while hour < 24:
            for i in range(2):
                power_consumed = power_consumed_total
                power_consumed += random.uniform(power_consumed_range_min, power_consumed_range_max)
                # power_consumed =  power_consumed
                average_voltage = random.randint(voltage_min, voltage_max)
                average_current = random.uniform(current_min, current_max)
                average_power_factor = random.uniform(power_factor_min, power_factor_max)
                within_a_day_obj = models.WithinADayData(consumer_id=1,
                                                         year=date_pointer.year,
                                                         month=date_pointer.month,
                                                         week=date_pointer.isocalendar()[1],
                                                         day=date_pointer.day,
                                                         hour=hour,
                                                         power_consumed=power_consumed,
                                                         average_voltage=average_voltage,
                                                         average_current=average_current,
                                                         average_power_factor=average_power_factor)
                within_a_day_obj.save()
                power_consumed_total = power_consumed
                last_bill = models.Bill.objects.filter(consumer_id=1).last()
                if last_bill is not None:
                    last_bill_reading = last_bill.present_bill_reading
                else:
                    last_bill_reading = 0
                units_consumed = power_consumed - last_bill_reading
                if 80 < units_consumed % 100 < 100 and last_message_sent_consumption != date_pointer:
                    message = models.Message(account_id=2,
                                             message=str(units_consumed) + " units have been consumed on " + str(
                                                 date_pointer))
                    message.save()
                    last_message_sent_consumption = date_pointer
                if average_power_factor < 0.7 and last_message_sent_pf != date_pointer:
                    message = models.Message(account_id=1,
                                             message="Power factor is " + str(
                                                 average_power_factor) + ", add Capacitive bank on " + str(
                                                 date_pointer))
                    message.save()
                    last_message_sent_pf = date_pointer
            hour += 1
        if previous_pointer is None:
            previous_pointer = date_pointer
            last_message_sent_consumption = date_pointer
            last_message_sent_pf = date_pointer
        else:
            # DayWiseData
            within_a_day_data = models.WithinADayData.objects.filter(consumer_id=1,
                                                                     year=previous_pointer.year,
                                                                     month=previous_pointer.month,
                                                                     day=previous_pointer.day)
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
            day_wise_data = models.DayWiseData(consumer_id=1,
                                               year=previous_pointer.year,
                                               month=previous_pointer.month,
                                               week=previous_pointer.isocalendar()[1],
                                               day=previous_pointer.day,
                                               power_consumed=power_consumed,
                                               average_voltage=average_voltage,
                                               average_current=average_current,
                                               average_power_factor=average_power_factor)
            day_wise_data.save()

            # WeekWiseData
            if date_pointer.isocalendar()[1] != previous_pointer.isocalendar()[1]:
                day_wise_data = models.DayWiseData.objects.filter(consumer_id=1,
                                                                  year=previous_pointer.year,
                                                                  month=previous_pointer.month,
                                                                  week=previous_pointer.isocalendar()[1])
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
                week_wise_data = models.WeekWiseData(consumer_id=1,
                                                     year=previous_pointer.year,
                                                     month=previous_pointer.month,
                                                     week=previous_pointer.isocalendar()[1],
                                                     power_consumed=power_consumed,
                                                     average_voltage=average_voltage,
                                                     average_current=average_current,
                                                     average_power_factor=average_power_factor)
                week_wise_data.save()
            # MonthWiseData
            if date_pointer.month != previous_pointer.month:
                week_wise_data = models.WeekWiseData.objects.filter(consumer_id=1,
                                                                    year=previous_pointer.year,
                                                                    month=previous_pointer.month)
                average_voltage = 0
                average_current = 0
                average_power_factor = 0
                power_consumed = 0
                # units_consumed = 0
                for obj in week_wise_data:
                    average_voltage += obj.average_voltage
                    average_current += obj.average_current
                    average_power_factor += obj.average_power_factor
                    power_consumed = obj.power_consumed
                average_voltage /= len(week_wise_data)
                average_current /= len(week_wise_data)
                average_power_factor /= len(week_wise_data)
                month_wise_data = models.MonthWiseData(consumer_id=1,
                                                       year=previous_pointer.year,
                                                       month=previous_pointer.month,
                                                       power_consumed=power_consumed,
                                                       average_voltage=average_voltage,
                                                       average_current=average_current,
                                                       average_power_factor=average_power_factor)
                month_wise_data.save()
                # Bill
                last_bill = models.Bill.objects.filter(consumer_id=1).last()
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

                bill = models.Bill(consumer_id=1, year=previous_pointer.year,
                                   last_bill_reading=last_bill_reading,
                                   present_bill_reading=power_consumed,
                                   power_consumption=units_consumed, bill_amount=price,
                                   paid=False)
                bill.save()
                previous_1_month_date = today.replace(day=1) - timedelta(days=1)
                previous_2_month_date = previous_1_month_date.replace(day=1) - timedelta(days=1)
                models.WithinADayData.objects.get(consumer_id=1, month=previous_2_month_date).delete()
                models.DayWiseData.objects.get(consumer_id=1, month=previous_2_month_date).delete()
                models.WeekWiseData.objects.get(consumer_id=1, month=previous_2_month_date).delete()
        previous_pointer += timedelta(days=1)
        date_pointer += timedelta(days=1)
