from datetime import datetime
import pycron


def test_parser():
    now = datetime(2015, 6, 18, 0, 9)
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
