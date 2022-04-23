#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid   = 2022-04-23
# author = Troy Williams
# email  = troy.williams@bluebill.net
# date   = fdc2997e-c307-11ec-bded-395f48fdf95d
# -----------

"""
Regex patterns used for discovering different date patterns in strings.
"""

# ------------
# System Modules - Included with Python

import re

# ------------
# 3rd Party - From PyPI

# ------------
# Custom Modules

# -------------


regex_strings = {}

# Date Strings used in utilities.date_from_string method
regex_strings["year"] = r"(?:[0-9]{4})"
regex_strings["month"] = r"(?:1[0-2]|0[1-9])"
regex_strings["day"] = r"(?:3[01]|0[1-9]|[12][0-9])"
regex_strings["isoweek"] = r"[1-9]|[0][1-9]|[1-4][0-9]|[5][0-3]"

# 1) year - yyyy - only match if it is the only thing in the string
regex_strings["year-only"] = r"^{}$".format(regex_strings["year"])


# 2) year-month - yyyy-mm - only match if it is the only thing in the string
regex_strings["year-month-only"] = r"^(?P<year>{})-(?P<month>{})$".format(
    regex_strings["year"], regex_strings["month"]
)

# 2.5) yyyy-mm-dd - only match if it is the only thing in the string
regex_strings["date-only"] = r"^(?P<year>{})-(?P<month>{})-(?P<day>{})$".format(
    regex_strings["year"], regex_strings["month"], regex_strings["day"]
)

# 3) isoweek - yyyyWnn - only match if it is the only thing in the string
regex_strings["isoweek-only"] = r"^(?P<year>{})[W|w](?P<week>{})$".format(
    regex_strings["year"], regex_strings["isoweek"]
)

# 4) week/offset - n
regex_strings["weekoffset-only"] = r"^0|(?:[-]\d*)$"

# 5) week - 01 to 53
regex_strings["week-only"] = r"^{}$".format(regex_strings["isoweek"])


# 6) Date range - yyyy-mm-dd to yyyy-mm-dd
regex_strings[
    "date-range"
] = r"^(?P<syear>{0})-(?P<smonth>{1})-(?P<sday>{2}) - (?P<eyear>{0})-(?P<emonth>{1})-(?P<eday>{2})$".format(
    regex_strings["year"],
    regex_strings["month"],
    regex_strings["day"],
)

# --------------
# compile regex
regex = {}

for k, v in regex_strings.items():
    regex[k] = re.compile(v)
