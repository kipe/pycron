import pycron
from datetime import datetime
from tests import test_day_names, test_dom, test_dow, test_has_been, test_hour, test_minute, test_month, test_random


print("testing minutes")
test_minute.test_minute()
test_minute.test_last_minute()
test_minute.test_minute_ranges()

print("testing hours")
test_hour.test_hour()

print("testing day of month")
test_dom.test_dom()

print("testing month")
test_month.test_parser()

print("testing numeric day of week")
test_dow.test_dow()
test_dow.test_day_matching()


print("testing day names")
test_day_names.test_day_matching()
test_day_names.test_day_names()

print("testing random expressions")
test_random.test_no_dt()
test_random.test_parse_arg()

print("test has_been functionality")
test_has_been.test_minutes()
test_has_been.test_hours()
test_has_been.test_days()
test_has_been.test_timezone()
test_has_been.test_raises()
