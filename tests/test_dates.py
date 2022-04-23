#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) <year> <copyright holders>

# uuid       = 5639a86a-b237-11ea-9bab-535c79fc3e3f
# author     = Troy Williams
# email      = troy.williams@bluebill.net
# date       = 2020-06-19
# -----------

"""
A module to test the utilities out.
"""

# ------------
# System Modules - Included with Python

from datetime import datetime as dt
from datetime import date
from datetime import time
from zoneinfo import ZoneInfo

# ------------
# 3rd Party - From pip

import pytest

# ------------
# Custom Modules

import notes.shared.dates as dts

# ------------



# Test - Iso-date (yyyy-mm-dd) Extraction

iso_dates = []

# No Matches
iso_dates.append(('2009', []))
iso_dates.append(('2009-001', []))
iso_dates.append(('2009-05', []))
iso_dates.append(('2009-123', []))
iso_dates.append(('2009-W511', []))
iso_dates.append(('20090621T0545Z', []))
iso_dates.append(('2009123', []))
iso_dates.append(('2009W511', []))

# Matches
iso_dates.append(('# 2020-09-18 - 2021-12-31', [date(2020, 9, 18), date(2021, 12, 31)]))
iso_dates.append(('2007-04-05T24:00', [date(2007, 4, 5)]))
iso_dates.append(('2007-04-06T00:00', [date(2007, 4, 6)]))
iso_dates.append(('2009-05-19T14:39Z', [date(2009, 5, 19)]))
iso_dates.append(('2010-02-18T16,2283', [date(2010, 2, 18)]))
iso_dates.append(('2010-02-18T16.23334444', [date(2010, 2, 18)]))
iso_dates.append(('2010-02-18T16:23,25', [date(2010, 2, 18)]))
iso_dates.append(('2010-02-18T16:23.4', [date(2010, 2, 18)]))
iso_dates.append(('2010-02-18T16:23:48,3-06:00', [date(2010, 2, 18)]))
iso_dates.append(('2010-02-18T16:23:48,444', [date(2010, 2, 18)]))
iso_dates.append(('2010-02-18T16:23:48.5', [date(2010, 2, 18)]))

@pytest.mark.parametrize('iso_date', iso_dates)
def test_find_all_iso_dates(iso_date):

    result = dts.find_all_iso_dates(iso_date[0])

    assert result == iso_date[1]

# -----------
# Date Range from Isoweek Testing

daterange_data = []
daterange_data.append((date(2020,7,24), (date(2020,7,20), date(2020,7,26))))
daterange_data.append((date(2020,7,26), (date(2020,7,20), date(2020,7,26))))
daterange_data.append((date(2020,7,20), (date(2020,7,20), date(2020,7,26))))

@pytest.mark.parametrize('search', daterange_data)
def test_isoweek_date_range_from_day(search):
    assert dts.isoweek_date_range_from_day(search[0]) == search[1]


# ----------
# isoweek date range

daterange_data = []
daterange_data.append(((2020, 30), (date(2020,7,20), date(2020,7,26))))
daterange_data.append(((2020, 29), (date(2020,7,13), date(2020,7,19))))
daterange_data.append(((2020, 31), (date(2020,7,27), date(2020,8,2))))

@pytest.mark.parametrize('search', daterange_data)
def test_isoweek_date_range(search):
    assert dts.isoweek_date_range(*search[0]) == search[1]

# ------------
# Isoweek offset

daterange_data = []
daterange_data.append(((2020, 30, -1), (2020, 29)))
daterange_data.append(((2020,  1, -1), (2019, 52)))
daterange_data.append(((2020, 30, -10), (2020, 20)))
daterange_data.append(((2020, 30, 62), (2021, 39)))

@pytest.mark.parametrize('search', daterange_data)
def test_isoweek_from_delta(search):
    assert dts.isoweek_from_delta(*search[0]) == search[1]

# ------------
# date_from_string testing

dfst_data = []

# yyyy
dfst_data.append(('1986', {'year':1986}))
dfst_data.append(('2025', {'year':2025}))
dfst_data.append(('0856', {'year':856}))


# yyyy-mm
dfst_data.append(('1986-12', {'year-month':(1986, 12)}))
dfst_data.append(('2019-11', {'year-month':(2019, 11)}))
dfst_data.append(('2019-01', {'year-month':(2019, 1)}))
dfst_data.append(('2019-05', {'year-month':(2019, 5)}))
dfst_data.append(('2019-09', {'year-month':(2019, 9)}))
dfst_data.append(('2019-9', None))
dfst_data.append(('1986-13', None))
dfst_data.append(('1986-133', None))
dfst_data.append(('1986--13', None))

# yyyy-mm-dd
dfst_data.append(('2019-11-22', {'year-month-day':(2019, 11, 22)}))
dfst_data.append(('0856-11-22', {'year-month-day':(856, 11, 22)}))
dfst_data.append(('2014-07-31', {'year-month-day':(2014, 7, 31)}))
dfst_data.append(('2019-11-35', None))

#yyyyWnn
dfst_data.append(('2019w11', {'year-week':(2019, 11)}))
dfst_data.append(('2019W11', {'year-week':(2019, 11)}))
dfst_data.append(('2020w35', {'year-week':(2020, 35)}))
dfst_data.append(('2020w1',  {'year-week':(2020, 1)}))
dfst_data.append(('202035', None))
dfst_data.append(('2012w45', {'year-week':(2012, 45)}))

# week offset
dfst_data.append(('0', {'week-offset':0}))
dfst_data.append(('-1', {'week-offset':-1}))
dfst_data.append(('-10', {'week-offset':-10}))
dfst_data.append(('-1 ', None))

# week number
dfst_data.append(('1', {'week-number':1}))
dfst_data.append(('01', {'week-number':1}))
dfst_data.append(('10', {'week-number':10}))
dfst_data.append(('100', None))


@pytest.mark.parametrize('search', dfst_data)
def test_date_from_string(search):
    assert dts.date_from_string(search[0]) == search[1]


