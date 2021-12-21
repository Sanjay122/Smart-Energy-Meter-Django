# importing date class from datetime module
from datetime import datetime
from . import models


def successful_insert_in_with_in_a_day_data(consumer):
    # creating the date object of today's date
    today = datetime.now()
    with_in_a_day_data_query_sets = models.WithinADayData.objects.filter(consumer=consumer, day=today)
    print(with_in_a_day_data_query_sets)
    print(len(with_in_a_day_data_query_sets))
