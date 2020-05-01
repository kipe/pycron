from datetime import datetime, timedelta
from enum import Enum
from typing import List
import calendar

DAY_NAMES = [x.lower() for x in calendar.day_name[6:] + calendar.day_name[:6]]
DAY_ABBRS = [x.lower() for x in calendar.day_abbr[6:] + calendar.day_abbr[:6]]
# Choice tuples, mainly designed to use with Django
MINUTE_CHOICES = [(str(x), str(x)) for x in range(0, 60)]
HOUR_CHOICES = [(str(x), str(x)) for x in range(0, 24)]
DOM_CHOICES = [(str(x), str(x)) for x in range(1, 32)]
MONTH_CHOICES = [(str(x), calendar.month_name[x]) for x in range(1, 13)]
DOW_CHOICES = [(str(i), day_name) for i, day_name in enumerate(DAY_NAMES)]


def _condition_in_range(value, accepted_values: set):
    return value in accepted_values


def _condition_equals(value, expected):
    return value == expected


def _condition_interval(value, expected, step):
    if expected is not None and value < expected:
        return False
    return value % step == 0


class CronTimeComparerArgumentCondition(object):
    action = None
    kwargs = None

    def __init__(self, action, **kwargs):
        super().__init__()

        self.action = action
        self.kwargs = kwargs

    def is_valid(self, value):
        return self.action(value, **self.kwargs)


class CronTimeComparer:
    def __init__(self, cron_time_string: str):
        super().__init__()
        self._cron_time_string = cron_time_string
        self._conditions = self.parse_cron_time_string(self._cron_time_string)
        compiled, lambda_exp = self.compile_conditions(self._conditions)
        self._invoke_conditions_compiled = compiled
        self._invoke_conditions_compiled_exp = lambda_exp

    @property
    def conditions(self) -> List[List[CronTimeComparerArgumentCondition]]:
        return self._conditions

    @staticmethod
    def compile_conditions(conditions: List[List[CronTimeComparerArgumentCondition]]):
        str_arr = []
        arg_idx = 0
        for arg_condition in conditions:
            if arg_condition is None or len(arg_condition) == 0:
                arg_idx += 1
                continue
            cond_str_arr = []
            arg_condition_idx = 0
            for arg_condition_part in arg_condition:
                cond_str_arr.append(f"conditions[{arg_idx}][{arg_condition_idx}].is_valid(v_{arg_idx})")
                arg_condition_idx += 1
            str_arr.append("(" + " or ".join(cond_str_arr) + ")")
            arg_idx += 1

        if len(str_arr) == 0:
            return True, None

        condition_string = " and ".join(str_arr)
        arg_names = map(lambda idx: f"v_{idx}", range(0, len(conditions)))
        lambda_exp = "lambda conditions, " + ",".join(arg_names) + ": " + condition_string
        lambda_method = eval(lambda_exp)
        return lambda_method, lambda_exp

    @staticmethod
    def to_int(value, is_day_of_week=False) -> int:
        """
        Converts a value to an integer. If is_day_of_week is True, it will convert day of week to an integer 0 through 6.
        @input:
            value = value to convert to integer
            is_day_of_week = True, to allow values like Mon or Monday
        @output: value as an integer
        """

        if isinstance(value, int) or (isinstance(value, str) and value.isnumeric()):
            return int(value)

        elif isinstance(value, str) and is_day_of_week and value in DAY_NAMES:
            return DAY_NAMES.index(value)

        elif isinstance(value, str) and is_day_of_week and value in DAY_ABBRS:
            return DAY_ABBRS.index(value)

        raise ValueError("Failed to parse string to integer")

    @staticmethod
    def try_to_int(value, is_day_of_week=False) -> int:
        try:
            return CronTimeComparer.to_int(value, is_day_of_week=is_day_of_week)
        except ValueError:
            return None

    @classmethod
    def parse_argument_parts(cls, arg: str, is_day_of_week=False) -> (any, int):
        arg = arg.strip()
        value = None
        step = None
        if "/" in arg:
            arg = arg.split("/")
            assert len(arg) == 2, ValueError("Time step must be defined as x/y. e.g. 54/2 or */2")

            value = arg[0] if arg[0] == "*" else cls.try_to_int(arg[0], is_day_of_week)
            step = cls.try_to_int(arg[1], is_day_of_week)

            assert value == "*" or value is not None, ValueError(f"Could not parse '{arg}' as a value. Expected x/y")
            assert step is not None, ValueError(f"Could not parse '{arg}' as a value. Expected x/y")
        elif arg == "*":
            value = arg
        else:
            value = cls.try_to_int(arg, is_day_of_week)
        return value, step

    @classmethod
    def parse_argument_conditions(
        cls, cron_time_arguments: str, max_value: int, is_day_of_week=False, min_value: int = 0
    ) -> List[CronTimeComparerArgumentCondition]:
        # In string form. The time arguments.
        cron_time_arguments = cron_time_arguments.strip()

        if cron_time_arguments == "*":
            # Any value will be true.
            return None

        cron_time_arguments = cron_time_arguments.split(",")

        arg_conditions = list()

        for cron_time_argument in cron_time_arguments:
            cron_time_argument = cron_time_argument.strip()

            if len(cron_time_argument) == 0:
                continue

            # extract the argument values.
            cron_time_argument_parts = None

            # Check for a range condition
            if "-" in cron_time_argument:
                cron_time_argument_parts = cron_time_argument.split("-")
                assert len(cron_time_argument_parts) == 2, ValueError(
                    "Time range arguments must be of the form, x-x, where x=number or x=a/b"
                )

                start_value, start_step = cls.parse_argument_parts(cron_time_argument_parts[0], is_day_of_week)
                end_value, step = cls.parse_argument_parts(cron_time_argument_parts[1], is_day_of_week)

                assert start_step is None and start_value is not None and start_value != "*", ValueError(
                    "In a time range (x-x) the start value must be a single number (no / and no '*')"
                )

                # special case for day of week.
                if is_day_of_week:
                    start_value = 0 if start_value == 7 else start_value
                    end_value = 0 if end_value == 7 else end_value

                if end_value == start_value:
                    # nothing to do here, is the whole thing.
                    # empty array means true.
                    continue

                step = step or 1
                accepted_values = []
                if end_value < start_value:
                    # move forward one.
                    end_value += max_value + 1
                    accepted_values += range(start_value, end_value + 1, step)
                else:
                    accepted_values = range(start_value, end_value + 1, step)

                accepted_values = set([v % (max_value + 1) for v in accepted_values])
                condition = CronTimeComparerArgumentCondition(_condition_in_range, accepted_values=accepted_values,)
                arg_conditions.append(condition)
            else:
                expected, step = cls.parse_argument_parts(cron_time_argument, is_day_of_week)
                condition = None
                if step != None:
                    expected = expected if expected != "*" else None
                    condition = CronTimeComparerArgumentCondition(_condition_interval, expected=expected, step=step)
                else:
                    condition = CronTimeComparerArgumentCondition(_condition_equals, expected=expected)

                arg_conditions.append(condition)

        if len(arg_conditions) == 0:
            # always true.
            return None

        return arg_conditions

    @classmethod
    def parse_cron_time_string(cls, cron_time_string: str) -> List[List[CronTimeComparerArgumentCondition]]:
        cron_time_string_args = list(filter(lambda v: len(v) > 0, cron_time_string.split(" ")))

        # args by order:
        # minute hour day_of_month month day_of_week
        # --
        # minute - 0 to 59, or *
        # hour - 0 to 23, or *
        # day_of_month - 1 to 31, or *
        # month - 1 to 12, or *
        # day_of_week - 0 to 7 (0 and 7 both represent Sunday), or * (no specific value)

        # autocomplete.
        while len(cron_time_string_args) < 5:
            cron_time_string_args.append("*")

        assert len(cron_time_string_args) <= 5, ValueError(
            f"Too many arguments in cron time string: {cron_time_string}"
        )

        condition_sets = [
            cls.parse_argument_conditions(cron_time_string_args[0], 59),
            cls.parse_argument_conditions(cron_time_string_args[1], 23),
            cls.parse_argument_conditions(cron_time_string_args[2], 31, min_value=1),
            cls.parse_argument_conditions(cron_time_string_args[3], 12, min_value=1),
            cls.parse_argument_conditions(cron_time_string_args[4], 6, is_day_of_week=True),
        ]

        return condition_sets

    def is_in_range_or_equals(self, dt: datetime):
        weekday = dt.isoweekday()
        if weekday == 7:
            weekday = 0

        if self._invoke_conditions_compiled is True:
            return True

        return self._invoke_conditions_compiled(self._conditions, dt.minute, dt.hour, dt.day, dt.month, weekday)


def is_now(s, dt=None):
    """
    A very simple cron-like parser to determine, if (cron-like) string is valid for this date and time.
    @input:
        s = cron-like string (minute, hour, day of month, month, day of week)
        dt = datetime to use as reference time, defaults to now
    @output: boolean of result
    """
    comp = CronTimeComparer(s)
    return comp.is_in_range_or_equals(dt or datetime.now())


def has_been(s, since, dt=None):
    """
    A parser to check whether a (cron-like) string has been true during a certain time period.
    Useful for applications which cannot check every minute or need to catch up during a restart.
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
