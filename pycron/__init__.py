from datetime import datetime, timedelta
import calendar


# Choice tuples, mainly designed to use with Django
MINUTE_CHOICES = [(str(x), str(x)) for x in range(0, 60)]
HOUR_CHOICES = [(str(x), str(x)) for x in range(0, 24)]
DOM_CHOICES = [(str(x), str(x)) for x in range(1, 32)]
MONTH_CHOICES = [(str(x), calendar.month_name[x]) for x in range(1, 13)]
DOW_CHOICES = [('0', calendar.day_name[6])] + [(str(x + 1), calendar.day_name[x]) for x in range(0, 6)]


def _parse_arg(value, target):
    value = value.strip()

    if value == '*':
        return True

    values = filter(None, [x.strip() for x in value.split(',')])

    for value in values:
        try:
            # First, try a direct comparison
            if int(value) == target:
                return True
        except ValueError:
            pass

        if '/' in value:
            v, interval = [x.strip() for x in value.split('/')]
            # Not sure if applicable for every situation, but just to make sure...
            if v != '*':
                continue
            # If the remainder is zero, this matches
            if target % int(interval) == 0:
                return True

        if '-' in value:
            try:
                start, end = [int(x.strip()) for x in value.split('-')]
            except ValueError:
                continue
            # If target value is in the range, it matches
            if target in range(start, end + 1):
                return True

    return False


def is_now(s, dt=None):
    '''
    A very simple cron-like parser to determine, if (cron-like) string is valid for this date and time.
    @input:
        s = cron-like string (minute, hour, day of month, month, day of week)
        dt = datetime to use as reference time, defaults to now
    @output: boolean of result
    '''
    if dt is None:
        dt = datetime.now()
    minute, hour, dom, month, dow = s.split(' ')
    weekday = dt.isoweekday()

    return _parse_arg(minute, dt.minute) \
        and _parse_arg(hour, dt.hour) \
        and _parse_arg(dom, dt.day) \
        and _parse_arg(month, dt.month) \
        and _parse_arg(dow, 0 if weekday == 7 else weekday)


def has_been(s, since, dt=None):
    '''
    A parser to check whether a (cron-like) string has been true during a certain time period.
    Useful for applications which cannot check every minute or need to catch up during a restart.
    @input:
        s = cron-like string (minute, hour, day of month, month, day of week)
        since = datetime to use as reference time for start of period
        dt = datetime to use as reference time for end of period, defaults to now
    @output: boolean of result
    '''
    if dt is None:
        dt = datetime.now(tz=since.tzinfo)

    if dt < since:
        raise ValueError("The since datetime must be before the current datetime.")

    while since <= dt:
        if is_now(s, since):
            return True
        since += timedelta(minutes=1)

    return False
