import pycron


def get_arg_result(arg, value, max_value, is_day_of_week=False):
    conditions = pycron.CronTimeComparer.parse_argument_conditions(
        arg, max_value=max_value, is_day_of_week=is_day_of_week
    )
    for cond in conditions:
        if cond.is_valid(value):
            return True
    return False


def test_parse_arg():
    assert get_arg_result("1/5", 0, max_value=12) is False
    assert get_arg_result("mon-wed", 0, max_value=6, is_day_of_week=True) is False


def test_no_dt():
    assert pycron.is_now("* * * * *")
