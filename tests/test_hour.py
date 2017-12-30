from datetime import datetime
import pycron
from pytz import utc
import pendulum
import arrow
import udatetime
from delorean import Delorean


def test_hour():
    def run(now):
        assert pycron.is_now('* * * * *', now)
        assert pycron.is_now('* 16 * * *', now)
        assert pycron.is_now('* */4 * * *', now)
        assert pycron.is_now('*/7 16 * * *', now)
        assert pycron.is_now('*/7 */8 * * *', now)
        assert pycron.is_now('* 2,8,16 * * *', now)
        assert pycron.is_now('* */9 * * *', now) is False
        assert pycron.is_now('* */5 * * *', now) is False
        assert pycron.is_now('*/3 */4 * * *', now) is False
        assert pycron.is_now('3 16 * * *', now) is False
        assert pycron.is_now('*/8 */3 * * *', now) is False
        assert pycron.is_now('* 2,8 * * *', now) is False
        assert pycron.is_now('* 16-20 * * *', now)
        assert pycron.is_now('* 0-10 * * *', now) is False

    now = datetime(2015, 6, 18, 16, 7)
    run(now)
    run(now.replace(tzinfo=utc))
    run(pendulum.instance(now))
    run(arrow.get(now))
    run(udatetime.from_string(now.isoformat()))
    run(Delorean(datetime=now, timezone='UTC').datetime)
