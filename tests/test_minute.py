from datetime import datetime
import pycron
from pytz import utc
import pendulum
import arrow
import udatetime
from delorean import Delorean


def test_minute():
    def run(now):
        assert pycron.is_now('* * * * *', now)
        assert pycron.is_now('9 * * * *', now)
        assert pycron.is_now('*/1 * * * *', now)
        assert pycron.is_now('*/3 * * * *', now)
        assert pycron.is_now('*/9 * * * *', now)
        assert pycron.is_now('3,9,25,16 * * * *', now)
        assert pycron.is_now('*/2 * * * *', now) is False
        assert pycron.is_now('*/4 * * * *', now) is False
        assert pycron.is_now('*/5 * * * *', now) is False
        assert pycron.is_now('*/12 * * * *', now) is False
        assert pycron.is_now('3,25,16 * * * *', now) is False
        assert pycron.is_now('0-10 * * * *', now)
        assert pycron.is_now('0-10 0-10 * * *', now)
        assert pycron.is_now('10-20 * * * *', now) is False
        assert pycron.is_now('10-20 10-20 * * *', now) is False
        assert pycron.is_now('1,2,5-10 * * * *', now)
        assert pycron.is_now('9,5-8 * * * *', now)
        assert pycron.is_now('10,20-30 * * * *', now) is False

        # Issue 14
        assert pycron.is_now('1-59/2 * * * *', now) is True
        assert pycron.is_now('1-59/4 * * * *', now) is True
        assert pycron.is_now('1-59/8 * * * *', now) is True

    now = datetime(2015, 6, 18, 0, 9)
    run(now)
    run(now.replace(tzinfo=utc))
    run(pendulum.instance(now))
    run(arrow.get(now))
    run(udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=now, timezone='UTC').datetime)


def test_last_minute():
    def run(now):
        assert pycron.is_now('* * * * *', now)
        assert pycron.is_now('59 * * * *', now)
        assert pycron.is_now('*/1 * * * *', now)
        # Issue 14
        assert pycron.is_now('1-59/2 * * * *', now) is True

    now = datetime(2015, 6, 18, 0, 59)
    run(now)
    run(now.replace(tzinfo=utc))
    run(pendulum.instance(now))
    run(arrow.get(now))
    run(udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=now, timezone='UTC').datetime)


def test_minute_ranges():
    for i in range(1, 59, 2):
        now = datetime(2015, 6, 18, 0, i)
        assert pycron.is_now('1-59/2 * * * *', now)
        assert pycron.is_now('1-59/2 * * * *', now.replace(tzinfo=utc))
        assert pycron.is_now('1-59/2 * * * *', pendulum.instance(now))
        assert pycron.is_now('1-59/2 * * * *', arrow.get(now))
        assert pycron.is_now('1-59/2 * * * *', udatetime.from_string(now.isoformat()))
        assert pycron.is_now('1-59/2 * * * *', Delorean(datetime=now, timezone='UTC').datetime)

    for i in range(0, 59, 2):
        now = datetime(2015, 6, 18, 0, i)
        assert pycron.is_now('1-59/2 * * * *', now) is False
        assert pycron.is_now('1-59/2 * * * *', now.replace(tzinfo=utc)) is False
        assert pycron.is_now('1-59/2 * * * *', pendulum.instance(now)) is False
        assert pycron.is_now('1-59/2 * * * *', arrow.get(now)) is False
        assert pycron.is_now('1-59/2 * * * *', udatetime.from_string(now.isoformat())) is False
        assert pycron.is_now('1-59/2 * * * *', Delorean(datetime=now, timezone='UTC').datetime) is False
