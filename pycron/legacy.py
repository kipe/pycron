from datetime import datetime, timedelta
import calendar

DAY_NAMES = [x.lower() for x in calendar.day_name[6:] + calendar.day_name[:6]]
DAY_ABBRS = [x.lower() for x in calendar.day_abbr[6:] + calendar.day_abbr[:6]]
# Choice tuples, mainly designed to use with Django
MINUTE_CHOICES = [(str(x), str(x)) for x in range(0, 60)]
HOUR_CHOICES = [(str(x), str(x)) for x in range(0, 24)]
DOM_CHOICES = [(str(x), str(x)) for x in range(1, 32)]
MONTH_CHOICES = [(str(x), calendar.month_name[x]) for x in range(1, 13)]
DOW_CHOICES = [(str(i), day_name) for i, day_name in enumerate(DAY_NAMES)]


def _to_int(value, allow_daynames=False):
    """
    Converts a value to an integer. If allow_daynames is True, it will convert day of week to an integer 0 through 6.
    @input:
        value = value to convert to integer
        allow_daynames = True, to allow values like Mon or Monday
    @output: value as an integer
    """

    if isinstance(value, int) or (isinstance(value, str) and value.isnumeric()):
        return int(value)

    elif isinstance(value, str) and allow_daynames and value in DAY_NAMES:
        return DAY_NAMES.index(value)

    elif isinstance(value, str) and allow_daynames and value in DAY_ABBRS:
        return DAY_ABBRS.index(value)

    raise ValueError('Failed to parse string to integer')


def _parse_arg(value, target, allow_daynames=False):
    value = value.strip()

    if value == '*':
        return True

    values = filter(None, [x.strip() for x in value.split(',')])

    for value in values:
        try:
            # First, try a direct comparison
            if _to_int(value, allow_daynames=allow_daynames) == target:
                return True
        except ValueError:
            pass

        if '-' in value:
            step = 1
            if '/' in value:
                # Allow divider in values, see issue #14
                try:
                    start, tmp = [
                        x.strip()
                        for x in value.split('-')
                    ]
                    start = _to_int(start)
                    end, step = [
                        _to_int(x.strip(), allow_daynames=allow_daynames)
                        for x in tmp.split('/')
                    ]
                except ValueError:
                    continue
            else:
                try:
                    start, end = [
                        _to_int(x.strip(), allow_daynames=allow_daynames)
                        for x in value.split('-')
                    ]
                except ValueError:
                    continue

            # If target value is in the range, it matches
            if target in range(start, end + 1, step):
                return True

            # Special cases, where the day names are more or less incorrectly set...
            if allow_daynames and start > end:
                return target in range(start, end + 6 + 1)

        if '/' in value:
            v, interval = [x.strip() for x in value.split('/')]
            # Not sure if applicable for every situation, but just to make sure...
            if v != '*':
                continue
            # If the remainder is zero, this matches
            if target % _to_int(interval, allow_daynames=allow_daynames) == 0:
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
        and _parse_arg(dow, 0 if weekday == 7 else weekday, True)


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
