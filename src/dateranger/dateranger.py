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

# import calendar

import pendulum

from datetime import date
from typing import Optional, Generator

# ------------
# 3rd Party - From PyPI

# ------------
# Custom Modules

from . import datestr as dts

# -------------

def date_range_from_year(year:int) -> pendulum.interval:
    """
    Given a year, return a tuple containing the start and end date of
    the year.
    """

    return pendulum.interval(
        sd:= pendulum.date(year, 1, 1),
        sd.end_of('year'),
    )


def date_range_from_year_month(
        year:int,
        month:int) -> pendulum.interval:
    """
    Given a year and a month, return a tuple containing the start and
    end date of the month.
    """

    return pendulum.interval(
        sd := pendulum.date(year, month, 1),
        sd.end_of('month'),
    )


def date_range_from_day(
        year:int,
        month:int,
        day:int) -> pendulum.interval:
    """
    Given a year, a month and a day, return a tuple containing the start
    and end date of the day

    NOTE: The start and end will be the same.
    """

    return pendulum.interval(
        d := pendulum.date(year, month, day),
        d,
    )


def date_range_from_week(year:int, week:int) -> pendulum.interval:
    """
    Given a year and a isoweek number, return a tuple containing the
    start and end date of the week.

    """

    sd = date.fromisocalendar(year, week, 1)  # Monday
    sd = pendulum.date(sd.year, sd.month, sd.day)

    ed = sd.end_of('week')

    return pendulum.interval(sd, ed)


def date_range_from_weekoffset(
        year:int,
        week:int,
        offset:int) -> pendulum.interval:
    """
    Given a year, a week and a week offset (0, -1, -2, ... -n), return a
    tuple containing the start and end date of the week.
    """

    # Find the Monday from the iso_year and iso_week
    sd = date.fromisocalendar(year, week, 1)
    sd = pendulum.date(sd.year, sd.month, sd.day)

    sd = sd.add(weeks=offset)
    ed = sd.end_of('week')

    return pendulum.interval(sd, ed)

def weeks_from_date_range(
        start_date:pendulum.date=None,
        end_date:pendulum.date=None
        ) -> Generator:
    """
    Given a start and end date, iterate through the weeks. It will
    return the start and end date for each isoweek.
    """

    period = pendulum.interval(start_date, end_date)

    for dt in period.range('weeks'):

        year, week, _ = dt.isocalendar()
        yield date_range_from_week(year, week)


def date_range_str(
        user_date: str,
        today:date=pendulum.now().date()
    ) -> Optional[pendulum.interval]:
    """
    Takes the user date string and returns a time range tuple.

    # Args

    - user_date
        - The date range string provided by the user

        - The possibilities are:

        - yyyy - A 4 digit year -> -> 0000 - 9999

        - yyyy-mm - An isoyear-iso month

        - yyyyWnn - Isoweek, week (2022W05)

        - yyyy-mm-dd - Isodate

        - n - Week number - 1 to 53
            - assumes current year

        - n - Relative week offset (0, -1, -2)
            - The relative week less than or equal to 0,

        - yyyy-mm-dd - yyyy-mm-dd - Date Range/Period/Duration

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

            start_date = pendulum.date(*sd)
            end_date = pendulum.date(*ed)

        except ValueError as ve:
            raise ValueError(f"{user_date} contains an invalid date!") from ve

        return pendulum.interval(start_date, end_date)

    return None
