import unittest
from datetime import datetime
import pycron
from pytz import utc
import pendulum
import arrow
import udatetime
from delorean import Delorean


class DOMTestCase(unittest.TestCase):
    def test_dom(self):
        def run(now):
            assert pycron.is_now("* * * * *", now)
            assert pycron.is_now("* * 18 * *", now)
            # Steps count from the 1st, so */6 is the 1st, 7th, 13th, 19th...
            # and the 18th is not one of those.
            assert pycron.is_now("* * */6 * *", now) is False
            assert pycron.is_now("* * 1,16,18 * *", now)
            assert pycron.is_now("* * 19 * *", now) is False
            assert pycron.is_now("* * */4 * *", now) is False
            assert pycron.is_now("* * 1,16 * *", now) is False
            assert pycron.is_now("* * 1,16 * *", now) is False
            assert pycron.is_now("* * 1-20 * *", now)
            assert pycron.is_now("* * 20-31 * *", now) is False

        now = datetime(2015, 6, 18, 16, 7)
        run(now)
        run(now.replace(tzinfo=utc))
        run(pendulum.instance(now))
        run(arrow.get(now))
        run(udatetime.from_string(now.isoformat()))
        run(Delorean(datetime=now, timezone="UTC").datetime)

    def test_dom_step(self):
        # */6 is just a shorthand for 1-31/6, both start counting from the 1st.
        assert pycron.is_now("* * */6 * *", datetime(2015, 6, 1, 16, 7))
        assert pycron.is_now("* * */6 * *", datetime(2015, 6, 7, 16, 7))
        assert pycron.is_now("* * */6 * *", datetime(2015, 6, 19, 16, 7))
        assert pycron.is_now("* * */6 * *", datetime(2015, 6, 6, 16, 7)) is False
        assert pycron.is_now("* * 1-31/6 * *", datetime(2015, 6, 7, 16, 7))
