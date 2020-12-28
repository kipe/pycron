# pycron
![Test Status](https://github.com/kipe/pycron/workflows/Test/badge.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/kipe/pycron/badge.svg?branch=master)](https://coveralls.io/github/kipe/pycron?branch=master)

Simple cron-like parser for Python, which determines if current datetime matches conditions.

## Installation
`pip install pycron`

## Usage
```python
import pycron
pycron.is_now('*/5 * * * *')  # True every 5 minutes
pycron.is_now('0 * * * *')    # True every hour, on minute 0
```

## Help
The formats currently supported are
- `*/5` (for "every X" function),
- `4-10` (for time ranges),
- `6,8,23` (for a list of values),
- `*` (for wildcard),
- and of course a single number.

The module includes `is_now(s, dt=None)`, where `s` is the cron-style string
and `dt` is the datetime to use (defaults to current datetime, if not set).
The function returns `True`, if `dt` matches the format.

It also includes `has_been(s, since, dt=None)`, where `s` is the cron-style string,
`since` is a datetime in the past and `dt` is the datetime to use (defaults to current datetime, if not set).
The function returns `True`, if `dt` would have matched the format at some point during the period.
This behaves much like like [anacron](https://en.wikipedia.org/wiki/Anacron) and is useful for applications which do not run continuously.

All functions are compatible with both timezone aware and naive datetimes.

There are couple of helpers available, mainly for use with Django.
They give out list of tuples, as required by Django field choices.

The available helpers are
- `pycron.MINUTE_CHOICES`,
- `pycron.HOUR_CHOICES`,
- `pycron.DOM_CHOICES`, for day of month
- `pycron.MONTH_CHOICES`, for month names
- `pycron.DOW_CHOICES`, for day names


## Support for alternative datetime -libraries
Currently supported "alternative" datetime libraries are:
- [Arrow](http://arrow.readthedocs.io/en/latest/)
- [Delorean](http://delorean.readthedocs.io/en/latest/)
- [Pendulum](https://pendulum.eustace.io/)
- [udatetime](https://github.com/freach/udatetime)


#### Notes
This was done, as I personally needed something like this to implement proper timers for my Django-project and
every available library felt too complicated for my use-case. Also, this was a good coding exercise...

As the Django -helper choices are quite limited, I've expanded them in my own project by adding values like
`('*/5', 'every 5 minutes')`, `('1-5', 'on weekdays')`, and `('0,6', 'on weekends')`.
I haven't included them in the code, as every use-case is different, this was just to give an idea on how to use this ;)
