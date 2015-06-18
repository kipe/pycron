from datetime import datetime


def _parse_arg(value, target, maximum):
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

        interval = int(interval)
        if interval not in range(0, maximum + 1):
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

    return _parse_arg(minute, now.minute, 30) \
        and _parse_arg(hour, now.hour, 12) \
        and _parse_arg(dom, now.day, 14) \
        and _parse_arg(month, now.month, 6) \
        and _parse_arg(dow, now.weekday(), 3)
