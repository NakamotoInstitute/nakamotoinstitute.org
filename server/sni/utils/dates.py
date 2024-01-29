import datetime

from zoneinfo import ZoneInfo


def date_to_localized_datetime(date: datetime.date, tz: str = "America/Chicago"):
    timezone = ZoneInfo(tz)
    return datetime.datetime(
        year=date.year, month=date.month, day=date.day, tzinfo=timezone
    )


def localize_time(time: datetime.datetime, tz: str = "America/Chicago"):
    if time.tzinfo is not None and time.tzinfo.utcoffset(time) is not None:
        raise ValueError(
            "Time already has timezone info, expected a naive datetime object."
        )

    localized_time = time.replace(tzinfo=ZoneInfo(tz))

    return localized_time
