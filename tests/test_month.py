from datetime import datetime
import pycron
from pytz import utc
import pendulum
import arrow
import udatetime
from delorean import Delorean


def test_parser():
    def run(now):
        assert pycron.is_now('* * * * *', now)
        assert pycron.is_now('* * * 6 *', now)
        assert pycron.is_now('* * * */2 *', now)
        assert pycron.is_now('* * * 1,4,6,12 *', now)
        assert pycron.is_now('* * * 5 *', now) is False
        assert pycron.is_now('* * * */5 *', now) is False
        assert pycron.is_now('* * * 1,4,12 *', now) is False
        assert pycron.MONTH_CHOICES[now.month - 1][1] == 'June'
        assert pycron.is_now('* * * 5-8 *', now)
        assert pycron.is_now('* * * 8-10 *', now) is False

    now = datetime(2015, 6, 18, 16, 7)
    run(now)
    run(now.replace(tzinfo=utc))
    run(pendulum.instance(now))
    run(arrow.get(now))
    run(udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=now, timezone='UTC').datetime)
