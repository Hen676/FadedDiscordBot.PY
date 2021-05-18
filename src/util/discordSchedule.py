#!/usr/bin/env python3.7

from datetime import datetime, timedelta
from typing import Optional


def _sleep_weekday(day: int) -> int:
    weekday = datetime.today().weekday()
    days = (7 - weekday) + day
    if days >= 7:
        days -= 7
    return timedelta(days=days).seconds


def _sleep_time(hour: int, minute: int) -> int:
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, hour, minute)
    if now.hour >= hour and now.minute > minute:
        future += timedelta(days=1)
    return (now - future).seconds


def sleep(hour: int, minute: int, weekday: Optional[int] = None) -> int:
    """
    Time to sleep until next weekday/hour/minute

    :param int hour: hour to start
    :param int minute: minute to start
    :param int weekday: 0-6 weekday to start
    :return: int sleep: time required to sleep until weekday/hour/minute
    """
    if weekday is not None:
        return _sleep_time(hour, minute) + _sleep_weekday(weekday)
    return _sleep_time(hour, minute)


def sleep_to_next_hour() -> int:
    """
    Time to sleep until next full hour

    :return: int sleep: time required to sleep to next hour
    """
    now = datetime.now()
    delta = timedelta(hours=1)
    next_hour = (now + delta).replace(microsecond=0, second=0, minute=0)
    return (next_hour - now).seconds
