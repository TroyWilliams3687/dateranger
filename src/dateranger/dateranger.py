#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid   = edc4b2c8-c307-11ec-bded-395f48fdf95d
# author = Troy Williams
# email  = troy.williams@bluebill.net
# date   = 2022-04-23
# -----------

"""
This module contains the `date_range_str` method. It will take a string
that contains a potential date range and return the date range. There
are also many help methods in this module.
"""

# ------------
# System Modules - Included with Python

import calendar

from datetime import date
from datetime import datetime as dt
from typing import Optional

# ------------
# 3rd Party - From PyPI

# ------------
# Custom Modules

from . import datestr as dts

# -------------

def date_range_from_year(year:int) -> tuple[date, date]:
    """
    Given a year, return a tuple containing the start and end date of
    the year.
    """

    return (date(year, 1, 1), date(year, 12, 31))


def date_range_from_year_month(
        year:int,
        month:int) -> tuple[date, date]:
    """
    Given a year and a month, return a tuple containing the start and
    end date of the month.
    """

    # start date is the first day of the month
    return (
        date(year, month, 1),
        date(year, month, calendar.monthrange(year, month)[-1]),
    )


def date_range_from_day(
        year:int,
        month:int,
        day:int) -> tuple[date, date]:
    """
    Given a year, a month and a day, return a tuple containing the start
    and end date of the day

    NOTE: The start and end will be the same.
    """

    # make sure this is valid
    d = date(year, month, day)

    return (d, d)


def date_range_from_week(year:int, week:int) -> tuple[date, date]:
    """
    Given a year and a isoweek number, return a tuple containing the
    start and end date of the week.

    """

    return dts.isoweek_date_range(year, week)


def date_range_from_weekoffset(
        year:int,
        week:int,
        offset:int) -> tuple[date, date]:
    """
    Given a year, a week and a week offset (0, -1, -2, ... -n), return a
    tuple containing the start and end date of the week.
    """

    return dts.isoweek_date_range(
        *dts.isoweek_from_delta(year, week, offset),
    )


def date_range_str(
        user_date: str,
        today:date=dt.now().date()
    ) -> Optional[tuple[date, date]]:
    """
    Takes the user date string and returns a time range tuple.

    # Args

    - user_date
        - The date range string provided by the user

        - The possibilities are:

        - A 4 digit year -> yyyy -> 0000 - 9999

        - An isoyear-iso month (yyyy-mm)

        - Isoweek (yyyyWnn), week (01 - 53)
            - assumes it is a week in the past of the current year

        - Isodate - a date in iso format (yyyy-mm-dd)

        - Week number - 1 to 53
            - assumes current year

        - Week offset (0, -1, -2)
            - the relative week less than or equal to 0,

        - date range
            - that is one yyyy-mm-dd to another ("yyyy-mm-dd to yyyy-mm-dd")

    # Return

    A tuple containing the start and end date

    """

    value = dts.date_from_string(user_date)

    if value is None:
        return None

    if (key:="year") in value:
        # value['year'] -> returns an integer
        return date_range_from_year(value[key])

    if (key:="year-month") in value:
        # value['year-month']-> tuple(int(year), int(mm))
        return date_range_from_year_month(*value[key])

    if (key:="year-month-day") in value:
        # value['year-month-day']-> tuple(int(year), int(mm), int(dd))
        try:

            return date_range_from_day(*value[key])

        except ValueError as ve:
            raise ValueError(f"{user_date} is an invalid date!") from ve

    if (key:="year-week") in value:
            # value['year-week'] -> tuple(int(year), int(week))
            return date_range_from_week(*value[key])

    if (key:="week-offset") in value:
        # value['week-offset']-> int

        iso_year, iso_week, _ = today.isocalendar()

        return date_range_from_weekoffset(
            iso_year,
            iso_week,
            value[key],
        )

    if (key:="week-number") in value:
        # value['week-number'] -> int

        iso_year, _, _ = today.isocalendar()

        return date_range_from_week(iso_year, value[key])

    if (key:="date-range") in value:

        sd, ed = value[key]

        try:

            start_date = date(*sd)
            end_date = date(*ed)

        except ValueError as ve:
            raise ValueError(f"{user_date} contains an invalid date!") from ve

        return (start_date, end_date)

    return None
