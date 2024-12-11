from .config import *

from datetime import datetime, timedelta

def get_num_days(start_date, end_date):
    date_format = "%Y.%m.%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    delta = end - start
    return delta.days

def get_end_date(start_date, num_days):
    date_format = "%Y.%m.%d"
    start = datetime.strptime(start_date, date_format)
    end = start + timedelta(days=num_days)
    return end.strftime(date_format)