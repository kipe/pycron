from datetime import datetime
import calendar


# Choice tuples, mainly designed to use with Django
MINUTE_CHOICES = [(str(x), str(x)) for x in range(0, 60)]
HOUR_CHOICES = [(str(x), str(x)) for x in range(0, 24)]
DOM_CHOICES = [(str(x), str(x)) for x in range(1, 32)]
MONTH_CHOICES = [(str(x), calendar.month_name[x]) for x in range(1, 13)]
DOW_CHOICES = [(str(x + 1), calendar.day_name[x]) for x in range(0, 7)]


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


def is_now(s):
    '''
    A very simple cron-like parser to determine, if (cron-like) string is valid for this date and time.
    @input: cron-like string (minute, hour, day of month, month, day of week)
    @output: boolean of result
    '''
    now = datetime.now()
    minute, hour, dom, month, dow = s.split(' ')

    return _parse_arg(minute, now.minute) \
        and _parse_arg(hour, now.hour) \
        and _parse_arg(dom, now.day) \
        and _parse_arg(month, now.month) \
        and _parse_arg(dow, now.weekday())
