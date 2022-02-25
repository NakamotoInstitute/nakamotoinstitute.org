from datetime import datetime

from pytz import timezone

TIMEZONE = timezone("US/Central")


def date_to_localized_datetime(date):
    time = datetime(year=date.year, month=date.month, day=date.day)
    return TIMEZONE.localize(time)


def localize_time(time):
    return TIMEZONE.localize(time)
