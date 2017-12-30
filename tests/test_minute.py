from datetime import datetime
import pycron
from pytz import utc


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

    now = datetime(2015, 6, 18, 0, 9)
    run(now)
    run(now.replace(tzinfo=utc))
