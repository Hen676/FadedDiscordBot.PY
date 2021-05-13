#!/usr/bin/env python3.7
"""
Created on Wed May  5 10:42:38 2021

config.py: shards config
"""
__author__ = "Henry John Timms"
__copyright__ = "Copyright 2021, Henry John Timms"
__license__ = "MIT"
__version__ = '1.0.0'

from datetime import datetime, timedelta
from typing import Optional


def _sleep_weekday(day: int):
    weekday = datetime.today().weekday()
    days = (7 - weekday) + day
    if days >= 7:
        days -= 7
    return timedelta(days=days).seconds


def _sleep_time(hour: int, minute: int):
    now = datetime.now()
    future = datetime(now.year, now.month, now.day, hour, minute)
    if now.hour >= hour and now.minute > minute:
        future += timedelta(days=1)
    return (now - future).seconds


def sleep(hour: int, minute: int, weekday: Optional[int] = None):
    """
    Time to sleep until next time specified

    :param int hour: hour to start
    :param int minute: minute to start
    :param int weekday: 0-6 weekday to start
    :return: int sleep: time required to sleep
    """
    if weekday is not None:
        return _sleep_time(hour, minute) + _sleep_weekday(weekday)
    return _sleep_time(hour, minute)
