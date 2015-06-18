from pycron import _parse_arg


def is_now(now, s):
    '''
    A very simple cron-like parser to determine, if (cron-like) string is valid for this date and time.
    @input: cron-like string
    @output: boolean of result
    '''
    minute, hour, dom, month, dow = s.split(' ')

    return _parse_arg(minute, now.minute) \
        and _parse_arg(hour, now.hour) \
        and _parse_arg(dom, now.day) \
        and _parse_arg(month, now.month) \
        and _parse_arg(dow, now.weekday())
