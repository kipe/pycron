from datetime import datetime, timedelta
import pycron
from pytz import utc
import pendulum
import arrow
import udatetime
from delorean import Delorean


def test_dow():
    def run(now):
        assert pycron.is_now('* * * * * *', now)
        assert pycron.is_now('* * * * * 169', now)
        assert pycron.is_now('* * * * * 1-365/2', now)
        assert pycron.is_now('* * * * * 168,169,170', now)
        assert pycron.is_now('* * * * * 170', now) is False
        assert pycron.is_now('* * * * * */2', now) is False
        assert pycron.is_now('* * * * * 165,166,167', now) is False
        assert pycron.is_now('* * * * 0-170', now)
        assert pycron.is_now('* * * * 170-365', now) is False

    now = datetime(2015, 6, 18, 16, 7)
    run(now)
    run(now.replace(tzinfo=utc))
    run(pendulum.instance(now))
    run(arrow.get(now))
    run(udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=now, timezone='UTC').datetime)
