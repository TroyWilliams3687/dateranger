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


from .regexpatterns import regex



def date_from_string(value: str) -> dict:
    """
    Given a string with the possibility of containing one of the
    accepted date formats return a dict containing the time range.

    # Args

    - value - The possibilities are:

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

    # year - yyyy
    if regex["year-only"].fullmatch(value):
        return {"year": int(value)}

    # year-month - yyyy-mm
    if match := regex["year-month-only"].fullmatch(value):
        return {"year-month": (int(match.group("year")), int(match.group("month")))}

    # yyyy-mm-dd
    if match := regex["date-only"].fullmatch(value):
        return {
            "year-month-day": (
                int(match.group("year")),
                int(match.group("month")),
                int(match.group("day")),
            )
        }

    # isoweek - yyyyWnn
    if match := regex["isoweek-only"].fullmatch(value):
        return {"year-week": (int(match.group("year")), int(match.group("week")))}

    # week/offset - n
    if match := regex["weekoffset-only"].fullmatch(value):
        return {"week-offset": int(value)}

    # week - 01 to 53
    if match := regex["week-only"].fullmatch(value):
        return {"week-number": int(value)}

    # date range
    if match := regex["date-range"].fullmatch(value):
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
