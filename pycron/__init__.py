from datetime import datetime
import calendar


# Choice tuples, mainly designed to use with Django
MINUTE_CHOICES = [(str(x), str(x)) for x in range(0, 60)]
HOUR_CHOICES = [(str(x), str(x)) for x in range(0, 24)]
DOM_CHOICES = [(str(x), str(x)) for x in range(1, 32)]
MONTH_CHOICES = [(str(x), calendar.month_name[x]) for x in range(1, 13)]
DOW_CHOICES = [('0', calendar.day_name[6])] + [(str(x + 1), calendar.day_name[x]) for x in range(0, 6)]


def _parse_arg(value, target):
    if value == '*':
        return True

    if ',' in value:
        if '*' in value:
            raise ValueError

        values = [int(x.strip()) for x in value.split(',')]
        if target in values:
            return True
        return False

    if '/' in value:
        value, interval = value.split('/')
        if value != '*':
            raise ValueError
        return target % int(interval) == 0

    if int(value) == target:
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
