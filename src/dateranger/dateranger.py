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
"""

# ------------
# System Modules - Included with Python

from datetime import datetime, date

# ------------
# 3rd Party - From PyPI

# ------------
# Custom Modules

import .datestr as DTS

# -------------

def date_range_from_year(year):
    """
    Given a year, return a tuple containing the start and end date of the year.
    """

    return (date(year, 1, 1), date(year, 12, 31))


def date_range_from_year_month(year, month):
    """
    Given a year-month, return a tuple containing the start and end date of the month.
    """

    # start date is the first day of the month
    return (
        date(year, month, 1),
        date(year, month, calendar.monthrange(year, month)[-1]),
    )


def date_range_from_day(year, month, day):
    """
    Given a year-month, return a tuple containing the start and end date of the day
    - the start and end will be the same.

    """

    # make sure this is valid
    d = date(year, month, day)

    return (d, d)


def date_range_from_week(year, week):
    """
    Given a year-week, return a tuple containing the start and end date of the week.

    """

    return dts.isoweek_date_range(year, week)


def date_range_from_weekoffset(year, week, offset):
    """
    Given a week offset (0, -1, -2, ... -n), return a tuple containing the start and end date of the week.
    """

    return dts.isoweek_date_range(*dts.isoweek_from_delta(year, week, offset))


def handle_date_switch(user_date: str) -> tuple[datetime, datetime]:
    """
    This method is designed to handle the --date switch option where the user can
    enter a string that represents some sort of date range they are interested in.

    The date of interest can be of the form:
    1. A 4 digit year -> yyyy -> 0000 - 9999
    2. An isoyear-iso month (yyyy-mm)
    3. Isoweek (yyyyWnn), week (01 - 53) - assumes it is a week in the past of the current year
    4. Isodate - a date in iso format (yyyy-mm-dd)
    5. Week number - 1 to 53 - assumes current year
    6. Week offset (0, -1, -2) - the relative week less than or equal to 0,
    6. date range (yyyy-mm-dd-yyyy-mm-dd) - start date and end date


    # Parameter

    user_date - str
        - the date type they are interested in using. It follows the above list

    # Return

    A list containing the start and end date to the range provided by the user.

    This ranges returned will be:
    1. yyyy-01-01 to yyyy-12-31
    2. yyyy-mm-01 to yyyy-mm-XX where XX will be the last day of the month
    3. yyyy-mm-XX to yyyy-mm-YY where XX will be the start of the iso week and YY will be the end of the isoweek. The month and year will change appropriately
    4. yyyy-mm-dd to yyyy-mm-dd
    5. See 3. -> Just a different way of specifying the week number
    6. See 3. -> Just a different way of specifying the week number
    7. 1234-12-01 to 1235-12-31

    """

    dates = []

    value = dts.date_from_string(user_date)

    if value:

        today = dt.now().date()

        iso_year_current, iso_week_current, _ = today.isocalendar()

        if "year" in value:
            # value['year'] -> returns an integer
            dates.extend(date_range_from_year(value["year"]))

        if "year-month" in value:
            # value['year-month']-> tuple(int(year), int(mm))
            dates.extend(date_range_from_year_month(*value["year-month"]))

        if "year-month-day" in value:
            # value['year-month-day']-> tuple(int(year), int(mm), int(dd))

            try:

                dates.extend(date_range_from_day(*value["year-month-day"]))

            except ValueError as ve:

                raise Value(f"{user_date} is an invalid date!") from ve

        if "year-week" in value:
            # value['year-week'] -> tuple(int(year), int(week))

            dates.extend(date_range_from_week(*value["year-week"]))

        if "week-offset" in value:
            # value['week-offset']-> int

            dates.extend(
                date_range_from_weekoffset(
                    iso_year_current, iso_week_current, value["week-offset"]
                )
            )

        if "week-number" in value:
            # value['week-number'] -> int

            dates.extend(date_range_from_week(iso_year_current, value["week-number"]))

        if "date-range" in value:

            sd, ed = value["date-range"]

            dates.append(date(*sd))
            dates.append(date(*ed))

    return tuple(dates)
