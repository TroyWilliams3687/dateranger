#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2021 Troy Williams

# uuid       = 8d789104-c308-11ec-bded-395f48fdf95d
# author     = Troy Williams
# email      = troy.williams@bluebill.net
# date       = 2022-04-23
# -----------

"""
This module has methods that take strings and return structures that
represent the dates that were discovered.
"""

# ------------
# System Modules - Included with Python

from datetime import datetime as dt
from datetime import date
from datetime import timedelta

from .regexpatterns import regex


def isoweek_from_delta(
            iso_year: int,
            iso_week: int,
            week_number_offset: int
        ) -> tuple[int, int]:
    """
    Given the isoyear and isoweek  and the week number offset return the
    valid isoweek number.

    Example:

    2020W30 -1 -> 2020W29
    2020W01 -2 -> 2019W51

    # Args

    - iso_year - The year (YYYY)

    - iso_week - The week number

    - week_number_offset - The relative week offset from the given
      year/week combination. The week number offset is how many weeks
      before (negative) or after(positive) to calculate.

    # Return

    A tuple of containing the offset isoyear and week number

    """

    # Find the Monday from the iso_year and iso_week
    sd = date.fromisocalendar(iso_year, iso_week, 1)

    # determine the offset from delta (assuming delta can be positive or
    # negative)
    offset_date = sd + timedelta(weeks=week_number_offset)

    iso_year, iso_week, _ = offset_date.isocalendar()

    return iso_year, iso_week


def isoweek_date_range(
        iso_year: int,
        iso_week: int
    ) -> tuple[date, date]:
    """
    Given, the isoyear and isoweek number, return the start date and
    end date of the week.

    # Args

    - iso_year
        - The isoyear number (yyyy) we are interested in

    - iso_week
        - The isoweek number

    # Return

    A tuple containing the start date and end date for the isoweek and
    isoyear
    """

    # Python 3.8 or higher.... (year, week, day of week)
    sd = date.fromisocalendar(iso_year, iso_week, 1)  # Monday
    ed = date.fromisocalendar(iso_year, iso_week, 7)  # Sunday

    return sd, ed


def isoweek_date_range_from_day(
            day: date
        ) -> tuple[date, date]:
    """
    Given a date object, return the date range that represents the
    isoweek that the date falls in.

    # Args

    - day
        - The day within a week that we want the week date range for

    # Return

    A list of tuple containing the start date and end date for the
    isoweek containing the date passed as an argument

    # Note

    This method uses the iso 8601 conventions for week numbers and week
    start end days i.e. Monday = 1, Sunday = 7
    """

    iso_year, iso_week, _ = day.isocalendar()

    return isoweek_date_range(iso_year, iso_week)


def date_from_string(value: str) -> dict:
    """
    Given a string with the possibility of containing one of the
    accepted date formats return a dict containing the time range.


    # Args

    value - The possibilities are:

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

    It will return a dictionary with one of the following keys:

    - 'year' -> returns an integer

    - 'year-month' -> tuple(int(year), int(mm))

    - 'year-month-day' -> tuple(int(year), int(mm), int(dd))

    - 'year-week' -> tuple(int(year), int(week))

    - 'week-offset' -> int

    - 'week-number' -> int

    - 'date-range'
        -> tuple(tuple(int(year), int(mm), int(dd)), tuple(int(year), int(mm), int(dd)))
        - first element is the start date, second element is the end date

    # NOTE

    This method doesn't check some of the entries to see if they are
    valid. For example, if the date is of the form 2020-02-30, that
    string will be returned even though February doesn't have 30 days!

    The regex for:

    - the 4 digit year should be good

    - the regex for week number will need to be checked, whether that
      year has 52 or 53 weeks

    - the iso date will need to be checked

    """

    # NOTE: We need to validate what we can, what makes sense

    # 1) year - yyyy
    if regex["year-only"].fullmatch(value):
        return {"year": int(value)}

    # 2) year-month - yyyy-mm
    match = regex["year-month-only"].fullmatch(value)

    if match:
        return {"year-month": (int(match.group("year")), int(match.group("month")))}

    # 2.5) yyyy-mm-dd
    match = regex["date-only"].fullmatch(value)

    if match:
        return {
            "year-month-day": (
                int(match.group("year")),
                int(match.group("month")),
                int(match.group("day")),
            )
        }

    # 3) isoweek - yyyyWnn
    match = regex["isoweek-only"].fullmatch(value)

    if match:
        return {"year-week": (int(match.group("year")), int(match.group("week")))}

    # 4) week/offset - n
    match = regex["weekoffset-only"].fullmatch(value)

    if match:
        return {"week-offset": int(value)}

    # 5) week - 01 to 53
    match = regex["week-only"].fullmatch(value)

    if match:
        return {"week-number": int(value)}

    # 6) date range
    match = regex["date-range"].fullmatch(value)

    if match:
        return {
            "date-range": (
                (
                    int(match.group("syear")),
                    int(match.group("smonth")),
                    int(match.group("sday")),
                ),
                (
                    int(match.group("eyear")),
                    int(match.group("emonth")),
                    int(match.group("eday")),
                ),
            )
        }

    return None
