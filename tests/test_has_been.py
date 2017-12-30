from datetime import datetime, timedelta
from nose.tools import assert_raises
from pytz import utc
import pycron
import pendulum
import arrow
import udatetime
from delorean import Delorean


def test_minutes():
    def run(since, now):
        assert pycron.has_been('* * * * *', since, now)
        assert pycron.has_been('0 * * * *', since, now) is False
        assert pycron.has_been('1 * * * *', since, now)
        assert pycron.has_been('2 * * * *', since, now)
        assert pycron.has_been('3 * * * *', since, now)
        assert pycron.has_been('4 * * * *', since, now) is False

    since = datetime(2015, 6, 18, 0, 1)
    now = datetime(2015, 6, 18, 0, 3)
    run(since, now)
    run(since.replace(tzinfo=utc), now.replace(tzinfo=utc))
    run(pendulum.instance(since), pendulum.instance(now))
    run(arrow.get(since), arrow.get(now))
    run(udatetime.from_string(since.isoformat()), udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=since, timezone='UTC').datetime, Delorean(datetime=now, timezone='UTC').datetime)


def test_hours():
    def run(since, now):
        assert pycron.has_been('* * * * *', since, now)
        assert pycron.has_been('* 0 * * *', since, now) is False
        assert pycron.has_been('* 1 * * *', since, now)
        assert pycron.has_been('* 2 * * *', since, now)
        assert pycron.has_been('* 3 * * *', since, now)
        assert pycron.has_been('* 4 * * *', since, now) is False

    since = datetime(2015, 6, 18, 1, 0)
    now = datetime(2015, 6, 18, 3, 0)
    run(since, now)
    run(since.replace(tzinfo=utc), now.replace(tzinfo=utc))
    run(pendulum.instance(since), pendulum.instance(now))
    run(arrow.get(since), arrow.get(now))
    run(udatetime.from_string(since.isoformat()), udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=since, timezone='UTC').datetime, Delorean(datetime=now, timezone='UTC').datetime)


def test_days():
    def run(since, now):
        assert pycron.has_been('* * * * *', since, now)
        assert pycron.has_been('* * 0 * *', since, now) is False
        assert pycron.has_been('* * 1 * *', since, now)
        assert pycron.has_been('* * 2 * *', since, now)
        assert pycron.has_been('* * 3 * *', since, now)
        assert pycron.has_been('* * 4 * *', since, now) is False

    since = datetime(2015, 6, 1, 0, 0)
    now = datetime(2015, 6, 3, 0, 0)
    run(since, now)
    run(since.replace(tzinfo=utc), now.replace(tzinfo=utc))
    run(pendulum.instance(since), pendulum.instance(now))
    run(arrow.get(since), arrow.get(now))
    run(udatetime.from_string(since.isoformat()), udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=since, timezone='UTC').datetime, Delorean(datetime=now, timezone='UTC').datetime)


def test_raises():
    since = datetime(2016, 6, 1, 0, 0)
    now = datetime(2015, 6, 3, 0, 0)
    assert_raises(ValueError, pycron.has_been, '* * * * *', since, now)
    assert_raises(ValueError, pycron.has_been, '* * * * *', pendulum.instance(since), pendulum.instance(now))
    assert_raises(ValueError, pycron.has_been, '* * * * *', arrow.get(since), arrow.get(now))
    assert_raises(ValueError, pycron.has_been, '* * * * *', udatetime.from_string(since.isoformat()), udatetime.from_string(now.isoformat()))
    assert_raises(ValueError, pycron.has_been, '* * * * *', Delorean(datetime=since, timezone='UTC').datetime, Delorean(datetime=now, timezone='UTC').datetime)


def test_timezone():
    since = datetime.now(tz=utc) - timedelta(hours=1)
    now = datetime.now(tz=None)

    assert pycron.has_been('* * * * *', since)
    assert_raises(TypeError, pycron.has_been, '* * * * *', since, now)
