from datetime import datetime
import calendar


# Choice generators, mainly designed to use with Django
MINUTE_CHOICES = (
    ['*'] + [str(x) for x in range(0, 60)],
    ['every minute'] + [str(x) for x in range(0, 60)]
)
HOUR_CHOICES = (
    ['*'] + [str(x) for x in range(0, 24)],
    ['every hour'] + [str(x) for x in range(0, 24)]
)
DOM_CHOICES = (
    ['*'] + [str(x) for x in range(1, 32)],
    ['every day of month'] + [str(x) for x in range(1, 32)]
)
MONTH_CHOICES = (
    ['*'] + [str(x) for x in range(1, 13)],
    ['every month'] + list(calendar.month_name)
)
DOW_CHOICES = (
    ['*'] + [str(x) for x in range(1, 8)],
    ['every day of week'] + list(calendar.day_name)
)


def _parse_arg(value, target):
    if value == '*':
        return True

    if ',' in value:
        if '*' in value:
            raise ValueError

        values = filter(None, [int(x.strip()) for x in value.split(',')])
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
