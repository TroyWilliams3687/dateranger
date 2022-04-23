# dateranger

## Introduction

This is a tool that takes a string representing a date range and returns a dictionary or it can translate it to a date range. The interesting thing is this library can take many different strings representing different ranges or time periods and return the appropriate date range.

Takes a string representing some sort of date or date range in the form of:

    - A 4 digit year -> yyyy -> 0000 - 9999

    - An isoyear-iso month (yyyy-mm)

    - Isoweek (yyyyWnn), week (01 - 53)
        - assumes it is a week in the past of the current year

    - Isodate - a date in iso format (yyyy-mm-dd)

    - Week number - 1 to 53
        - Assumes current year

    - Week offset (0, -1, -2)
        - The relative week less than or equal to 0,

    - date range
        - that is one yyyy-mm-dd to another ("yyyy-mm-dd to yyyy-mm-dd")

    It will return a dictionary with one of the following keys:

    - 'year' -> returns an integer

    - 'year-month' -> tuple(int(year), int(mm))

    - 'year-month-day' -> tuple(int(year), int(mm), int(dd))

    - 'year-week' -> tuple(int(year), int(week))

    - 'week-offset' -> int

    - 'week-number' -> int

    - 'date-range' -> tuple(tuple(int(year), int(mm), int(dd)), tuple(int(year), int(mm), int(dd)))
        - first element is the start date, second element is the end date



## Usage

Build the virtual environment or run the tests with the [make](make.md) files and use the module like:

```python
>>> from dateranger.dateranger import date_range_str

>>> date_range_str('2020-01-01 - 2020-07-31')
(date(2020,1,1),date(2020,7,31))

>>> date_range_str('2022W03')
(date(2022,1,17),date(2022,1,23))
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

