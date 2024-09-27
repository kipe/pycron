import unittest
from datetime import datetime
import pycron
from pytz import utc
import pendulum
import arrow
import udatetime
from delorean import Delorean


class DOMDOWTestCase(unittest.TestCase):
    def test_dom(self):
        def run(now):
            assert pycron.is_now("* * * * *", now)
            assert pycron.is_now("* * 22 * thu", now)
            assert pycron.is_now("* * 23 * thu", now)
            assert pycron.is_now("* * 23 * fri", now)
            assert pycron.is_now("* * 23 * *", now)
            assert pycron.is_now("* * * * thu", now)
            assert pycron.is_now("* * * * *", now)
            assert pycron.is_now("* * * * fri", now) is False
            assert pycron.is_now("* * 22 * *", now) is False

        now = datetime(2022, 6, 23, 16, 44)  # Thursday
        run(now)
        run(now.replace(tzinfo=utc))
        run(pendulum.instance(now))
        run(arrow.get(now))
        run(udatetime.from_string(now.isoformat()))
        run(Delorean(datetime=now, timezone="UTC").datetime)
