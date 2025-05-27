"""Simple cron-like parser, which determines if current datetime matches conditions."""

from datetime import datetime, timedelta
import calendar
from typing import Any, Optional

DAY_NAMES = [x.lower() for x in [*calendar.day_name[6:], *calendar.day_name[:6]]]
DAY_ABBRS = [x.lower() for x in [*calendar.day_abbr[6:], *calendar.day_abbr[:6]]]
# Choice tuples, mainly designed to use with Django
MINUTE_CHOICES = [(str(x), str(x)) for x in range(0, 60)]
HOUR_CHOICES = [(str(x), str(x)) for x in range(0, 24)]
DOM_CHOICES = [(str(x), str(x)) for x in range(1, 32)]
MONTH_CHOICES = [(str(x), calendar.month_name[x]) for x in range(1, 13)]
DOW_CHOICES = [(str(i), day_name) for i, day_name in enumerate(DAY_NAMES)]


def _to_int(value: Any, allow_daynames: bool = False) -> int:
    """
    Converts a value to an integer.
    If allow_daynames is True, it will convert day of week to an integer 0 through 6.

    @input:
        value = value to convert to integer
        allow_daynames = True, to allow values like Mon or Monday
    @output: value as an integer
    """

    if isinstance(value, int) or (isinstance(value, str) and value.isnumeric()):
        return int(value)

    if isinstance(value, str) and allow_daynames and value.lower() in DAY_NAMES:
        return DAY_NAMES.index(value.lower())

    if isinstance(value, str) and allow_daynames and value.lower() in DAY_ABBRS:
        return DAY_ABBRS.index(value.lower())

    raise ValueError("Failed to parse string to integer")


def _parse_arg(value: str, target: int, allow_daynames: bool = False) -> bool:
    """
    Parses a given value and checks if it matches the provided target.
    Allowing day names is optional, but can be useful for certain situations.

    @input:
        value = value to parse and check
        target = target value to compare with
        allow_daynames = True, to allow values like Mon or Monday
    @output: True if the value matches the target, False otherwise
    """
    # pylint: disable=too-many-branches
    value = value.strip()

    if value == "*":
        return True

    values = filter(None, [x.strip() for x in value.split(",")])

    for _value in values:
        try:
            # First, try a direct comparison
            if _to_int(_value, allow_daynames=allow_daynames) == target:
                return True
        except ValueError:
            pass

        if "-" in _value:
            step = 1
            if "/" in _value:
                # Allow divider in values, see issue #14
                try:
                    start, tmp = [x.strip() for x in _value.split("-")]
                    start_int = _to_int(start)
                    end, step = [
                        _to_int(x.strip(), allow_daynames=allow_daynames)
                        for x in tmp.split("/")
                    ]
                except ValueError:
                    continue
            else:
                try:
                    start_int, end = [
                        _to_int(x.strip(), allow_daynames=allow_daynames)
                        for x in _value.split("-")
                    ]
                except ValueError:
                    continue

            # If target value is in the range, it matches
            if target in range(start_int, end + 1, step):
                return True

            # Special cases, where the day names are more or less incorrectly set...
            if allow_daynames and start_int > end:
                return target in range(start_int, end + 6 + 1)

        if "/" in _value:
            v, interval = [x.strip() for x in _value.split("/")]
            # Not sure if applicable for every situation, but just to make sure...
            if v != "*":
                continue
            # If the remainder is zero, this matches
            if target % _to_int(interval, allow_daynames=allow_daynames) == 0:
                return True

    return False


def is_now(s: str, dt: Optional[datetime] = None) -> bool:
    """
    A very simple cron-like parser to determine, if (cron-like) string is valid
    for this date and time.

    @input:
        s = cron-like string (minute, hour, day of month, month, day of week)
        dt = datetime to use as reference time, defaults to now
    @output: boolean of result
    """
    if dt is None:
        dt = datetime.now()
    minute, hour, dom, month, dow = [x.strip() for x in s.split(" ")]
    weekday = dt.isoweekday()

    # Special case if both of the 'day' -fields are set -> allow either one to match
    # See: https://github.com/kipe/pycron/issues/29
    if "*" not in dom and "*" not in dow:
        day_rule = _parse_arg(dom, dt.day) or _parse_arg(
            dow, 0 if weekday == 7 else weekday, True
        )
    else:
        day_rule = _parse_arg(dom, dt.day) and _parse_arg(
            dow, 0 if weekday == 7 else weekday, True
        )

    return (
        _parse_arg(minute, dt.minute)
        and _parse_arg(hour, dt.hour)
        and _parse_arg(month, dt.month)
        and day_rule
    )


def has_been(s: str, since: datetime, dt: Optional[datetime] = None) -> bool:
    """
    A parser to check whether a (cron-like) string has been true
    during a certain time period.
    Useful for applications which cannot check every minute or need to
    catch up during a restart.

    @input:
        s = cron-like string (minute, hour, day of month, month, day of week)
        since = datetime to use as reference time for start of period
        dt = datetime to use as reference time for end of period, defaults to now
    @output: boolean of result
    """
    if dt is None:
        dt = datetime.now(tz=since.tzinfo)

    if dt < since:
        raise ValueError("The since datetime must be before the current datetime.")

    while since <= dt:
        if is_now(s, since):
            return True
        since += timedelta(minutes=1)

    return False
