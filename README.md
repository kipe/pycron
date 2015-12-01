# pycron [![Build Status](https://travis-ci.org/kipe/pycron.svg?branch=master)](https://travis-ci.org/kipe/pycron)
Simple cron-like parser, which determines if current datetime matches conditions

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

The module includes only one function, `is_now(s, dt=None)`, where `s` is the cron-style string
and `dt` is the datetime to use (defaults to current datetime, if not set).
The function returns `True`, if `dt` matches the format.

There are couple of helpers available, mainly for use with Django.
They give out list of tuples, as required by Django field choices.

The available helpers are
- `pycron.MINUTE_CHOICES`,
- `pycron.HOUR_CHOICES`,
- `pycron.DOM_CHOICES`, for day of month
- `pycron.MONTH_CHOICES`, for month names
- `pycron.DOW_CHOICES`, for day names


#### Notes
This was done, as I personally needed something like this to implement proper timers for my Django-project and
every available library felt too complicated for my use-case. Also, this was a good coding exercise...

As the Django -helper choices are quite limited, I've expanded them in my own project by adding values like
`('*/5', 'every 5 minutes')`, `('1-5', 'on weekdays')`, and `('0,6', 'on weekends')`.
I haven't included them in the code, as every use-case is different, this was just to give an idea on how to use this ;)
