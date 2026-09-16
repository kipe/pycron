from datetime import datetime
import unittest
import pycron
from pytz import utc
import pendulum
import arrow
import udatetime
from delorean import Delorean


class MonthTestCase(unittest.TestCase):
    def test_parser(self):
        def run(now):
            assert pycron.is_now("* * * * *", now)
            assert pycron.is_now("* * * 6 *", now)
            # Steps count from January, so */2 is Jan, Mar, May... and */5 is
            # Jan, Jun, Nov. June matches the second one, not the first.
            assert pycron.is_now("* * * */2 *", now) is False
            assert pycron.is_now("* * * 1,4,6,12 *", now)
            assert pycron.is_now("* * * 5 *", now) is False
            assert pycron.is_now("* * * */5 *", now)
            assert pycron.is_now("* * * 1,4,12 *", now) is False
            assert pycron.MONTH_CHOICES[now.month - 1][1] == "June"
            assert pycron.is_now("* * * 5-8 *", now)
            assert pycron.is_now("* * * 8-10 *", now) is False

        now = datetime(2015, 6, 18, 16, 7)
        run(now)
        run(now.replace(tzinfo=utc))
        run(pendulum.instance(now))
        run(arrow.get(now))
        run(udatetime.from_string(now.isoformat()))
        run(Delorean(datetime=now, timezone="UTC").datetime)

    def test_month_step(self):
        # */3 is just a shorthand for 1-12/3, both start counting from January.
        assert pycron.is_now("* * * */3 *", datetime(2015, 1, 18, 16, 7))
        assert pycron.is_now("* * * */3 *", datetime(2015, 4, 18, 16, 7))
        assert pycron.is_now("* * * */3 *", datetime(2015, 7, 18, 16, 7))
        assert pycron.is_now("* * * */3 *", datetime(2015, 6, 18, 16, 7)) is False
        assert pycron.is_now("* * * 1-12/3 *", datetime(2015, 4, 18, 16, 7))
