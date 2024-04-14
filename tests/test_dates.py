#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# -----------
# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Troy Williams

# uuid       = 5ae62494-c313-11ec-bded-395f48fdf95d
# author     = Troy Williams
# email      = troy.williams@bluebill.net
# date       = 2022-04-23
# -----------

"""
"""

# ------------
# System Modules - Included with Python


from datetime import date
# from datetime import time

# ------------
# 3rd Party - From pip

import pytest
import pendulum

# ------------
# Custom Modules

from dateranger.datestr import date_from_string
from dateranger.dateranger import date_range_str, weeks_from_date_range

# ------------
# 'year'

data = []
data.append(('year','2022', 2022))
data.append(('year','0000', 0))
data.append(('year','0105', 105))
data.append(('year','1974', 1974))

# ------------
# 'year-month'

data.append(('year-month','2022-03', (2022,3)))
data.append(('year-month','0000-04', (0,4)))
data.append(('year-month','0105-05', (105,5)))
data.append(('year-month','1974-07', (1974,7)))

# ------------
# 'year-month-day'

data.append(('year-month-day','2022-03-14', (2022,3,14)))
data.append(('year-month-day','0000-04-07', (0,4,7)))
data.append(('year-month-day','0105-05-22', (105,5,22)))
data.append(('year-month-day','1974-07-31', (1974,7,31)))

# ------------
# 'year-week'

data.append(('year-week','2022W03', (2022, 3)))
data.append(('year-week','0000W04', (0, 4)))
data.append(('year-week','0105W22', (105, 22)))
data.append(('year-week','1974W18', (1974, 18)))

# ------------
# 'week-offset' Valid from 0 to -n

data.append(('week-offset','-10', -10))
data.append(('week-offset','-5', -5))
data.append(('week-offset','0', 0))

# ------------
# 'week-number' - Valid from 01 to 53

data.append(('week-number','10', 10))
data.append(('week-number','5', 5))
data.append(('week-number','1', 1))
data.append(('week-number','53', 53))
data.append(('week-number','01', 1))
data.append(('week-number','05', 5))

# ------------
# 'date-range'

data.append(('date-range','1974-07-01 - 1974-07-31', ((1974,7,1), (1974,7,31))))
data.append(('date-range','1974-07-01 - 1974-07-05', ((1974,7,1), (1974,7,5))))
data.append(('date-range','2020-01-01 - 2020-07-31', ((2020,1,1), (2020,7,31))))

# ------------
# Test date_from_string - matches

@pytest.mark.parametrize('data', data)
def test_date_from_string_year(data):

    key, value, result = data

    assert date_from_string(value)[key] == result


# ===========
# ===========
# No Matches

# ------------
# 'year-month'

data = []
data.append(('year','YYYY', None))
data.append(('year','This is a test', None))
data.append(('year','', None))

# ------------
# 'year-month'

data.append(('year-month','2022-14', None))
data.append(('year-month','Hello World', None))
data.append(('year-month','105-05', None))

# ------------
# 'year-month-day'

data.append(('year-month-day','2022-13-14', None))
data.append(('year-month-day','0000-04-32', None))
data.append(('year-month-day','1974-0-31', None))

# ------------
# 'year-week'

data.append(('year-week','2022W55', None))
data.append(('year-week','0000W-04', None))


# ------------
# 'week-offset'

# data.append(('week-offset','-0-5', None))

# NOTE: Not really much to test here

# ------------
# 'week-number'

data.append(('week-number','54', None))

# ------------
# 'date-range'

data.append(('date-range','1974-07-01 - ', None))
data.append(('date-range',' - 1974-07-05', None))
data.append(('date-range','aeser-01-01 - 2020-07-31', None))
data.append(('date-range','2020-02-32 - 2020-07-31', None))


@pytest.mark.parametrize('data', data)
def test_date_from_string_year_no_matches(data):

    key, value, result = data

    assert date_from_string(value) is None

# ============
#  Testing date_from_str

data = []
data.append(('2022',       pendulum.interval(pendulum.date(2022,1,1), pendulum.date(2022,12,31))))
data.append(('2022-07',    pendulum.interval(pendulum.date(2022,7,1), pendulum.date(2022,7,31))))
data.append(('2022-07-31', pendulum.interval(pendulum.date(2022,7,31), pendulum.date(2022,7,31))))
data.append(('2022W03',    pendulum.interval(pendulum.date(2022,1,17),pendulum.date(2022,1,23))))
data.append(('2020-01-01 - 2020-07-31', pendulum.interval(pendulum.date(2020,1,1), pendulum.date(2020,7,31))))

# week offset
data.append((pendulum.date(2022, 3, 1), '-1', pendulum.interval(pendulum.date(2022,2,21),pendulum.date(2022,2,27))))

# Week number
data.append((pendulum.date(2022, 3, 1), '1', pendulum.interval(pendulum.date(2022,1,3),pendulum.date(2022,1,9))))

@pytest.mark.parametrize('data', data)
def test_date_from_str(data):

    match data:
        case (today, value, result):
            assert date_range_str(value, today=today) == result

        case (value, result):
            assert date_range_str(value) == result


# ============
#  Testing weeks_from_date_range

data = []

date_inputs = (
    pendulum.date(2022,1,4),
    pendulum.date(2022,2,4),
)

date_outputs = (
    pendulum.interval(pendulum.date(2022,1,3), pendulum.date(2022,1,9)),
    pendulum.interval(pendulum.date(2022,1,10), pendulum.date(2022,1,16)),
    pendulum.interval(pendulum.date(2022,1,17), pendulum.date(2022,1,23)),
    pendulum.interval(pendulum.date(2022,1,24), pendulum.date(2022,1,30)),
    pendulum.interval(pendulum.date(2022,1,31), pendulum.date(2022,2,6)),
)

data.append((date_inputs, date_outputs))



date_inputs = (
    pendulum.date(2021,12,18),
    pendulum.date(2022,1,10),
)

date_outputs = (
    pendulum.interval(pendulum.date(2021,12,13), pendulum.date(2021,12,19)),
    pendulum.interval(pendulum.date(2021,12,20), pendulum.date(2021,12,26)),
    pendulum.interval(pendulum.date(2021,12,27), pendulum.date(2022,1,2)),
    pendulum.interval(pendulum.date(2022,1,3), pendulum.date(2022,1,9)),
    pendulum.interval(pendulum.date(2022,1,10), pendulum.date(2022,1,16)),
)

data.append((date_inputs, date_outputs))


date_inputs = (
    date(2021,12,18),
    date(2022,1,10),
)

date_outputs = (
    pendulum.interval(date(2021,12,13), date(2021,12,19)),
    pendulum.interval(date(2021,12,20), date(2021,12,26)),
    pendulum.interval(date(2021,12,27), date(2022,1,2)),
    pendulum.interval(date(2022,1,3), date(2022,1,9)),
    pendulum.interval(date(2022,1,10), date(2022,1,16)),
)

data.append((date_inputs, date_outputs))

@pytest.mark.parametrize('data', data)
def test_weeks_from_date_range(data):

    inputs, outputs = data

    for results, output in zip(weeks_from_date_range(*inputs), outputs):
        assert results == output

