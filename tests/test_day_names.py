from datetime import datetime, timedelta
import pycron
from pytz import utc
import pendulum
import arrow
import udatetime
from delorean import Delorean


def test_day_names():
    def run(now):
        assert pycron.is_now('* * * * *', now)
        assert pycron.is_now('* * * * thu', now)
        assert pycron.is_now('* * * * thursday', now)
        assert pycron.is_now('* * * * */thu', now)
        assert pycron.is_now('* * * * */thursday', now)
        assert pycron.is_now('* * * * sun,wed,thu', now)
        assert pycron.is_now('* * * * sunday,wednesday,thursday', now)
        assert pycron.is_now('* * * * wed', now) is False
        assert pycron.is_now('* * * * wednesday', now) is False
        assert pycron.is_now('* * * * */wed', now) is False
        assert pycron.is_now('* * * * */wednesday', now) is False
        assert pycron.is_now('* * * * sun,wed,sat', now) is False
        assert pycron.is_now('* * * * sunday,wednesday,saturday', now) is False
        assert pycron.DOW_CHOICES[now.isoweekday()][1] == 'thursday'
        assert pycron.DOW_CHOICES[0][1] == 'sunday'
        assert pycron.is_now('* * * * sun-thu', now)
        assert pycron.is_now('* * * * sunday-thursday', now)
        assert pycron.is_now('* * * * fri-sat', now) is False
        assert pycron.is_now('* * * * friday-saturday', now) is False
        # Special cases, where the day names are more or less incorrectly set...
        assert pycron.is_now('* * * * thu-sun', now)
        assert pycron.is_now('* * * * thursday-sunday', now)
        assert pycron.is_now('* * * * wed-sun', now)
        assert pycron.is_now('* * * * wednesday-sunday', now)
        assert pycron.is_now('* * * * wed-mon', now)
        assert pycron.is_now('* * * * wednesday-monday', now)
        assert pycron.is_now('* * * * fri-sun', now) is False
        assert pycron.is_now('* * * * friday-sunday', now) is False
        assert pycron.is_now('* * * * fri-wed', now) is False
        assert pycron.is_now('* * * * friday-wednesday', now) is False

        # Test day matching for dividers
        assert pycron.is_now('* * * * monday-sunday/3', now) is False
        assert pycron.is_now('* * * * mon-sun/3', now) is False
        assert pycron.is_now('* * * * tuesday-sunday/2', now) is False
        assert pycron.is_now('* * * * tue-sun/2', now) is False

    now = datetime(2015, 6, 18, 16, 7)
    run(now)
    run(now.replace(tzinfo=utc))
    run(pendulum.instance(now))
    run(arrow.get(now))
    run(udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=now, timezone='UTC').datetime)


def test_day_matching():
    def run(now):
        for i in range(0, 7):
            # Test day matching from Sunday onwards...
            now += timedelta(days=1)
            assert pycron.is_now('* * * * %s' % (pycron.DAY_NAMES[i]), now)
            assert pycron.is_now('* * * * %s' % (pycron.DAY_ABBRS[i]), now)
            # Test weekdays
            assert pycron.is_now('* * * * mon,tue,wed,thu,fri',
                                 now) is (True if i not in [0, 6] else False)
            assert pycron.is_now('* * * * monday,tuesday,wednesday,thursday,friday',
                                 now) is (True if i not in [0, 6] else False)
            assert pycron.is_now(
                '* * * * mon-fri', now) is (True if i not in [0, 6] else False)
            assert pycron.is_now(
                '* * * * monday-friday', now) is (True if i not in [0, 6] else False)
            assert pycron.is_now('* * * * mon,tue,wed,thu-fri',
                                 now) is (True if i not in [0, 6] else False)
            assert pycron.is_now('* * * * monday,tuesday,wednesday,thursday-friday',
                                 now) is (True if i not in [0, 6] else False)
            # Test weekends
            assert pycron.is_now(
                '* * * * sun,sat', now) is (True if i in [0, 6] else False)
            assert pycron.is_now(
                '* * * * sunday,saturday', now) is (True if i in [0, 6] else False)

    now = datetime(2015, 6, 20, 16, 7)
    run(now)
    run(now.replace(tzinfo=utc))
    run(pendulum.instance(now))
    run(arrow.get(now))
    run(udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=now, timezone='UTC').datetime)
