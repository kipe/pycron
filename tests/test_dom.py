from datetime import datetime
import pycron


def test_parser():
    now = datetime(2015, 6, 18, 16, 7)
    assert pycron.is_now('* * * * *', now)
    assert pycron.is_now('* * 18 * *', now)
    assert pycron.is_now('* * */6 * *', now)
    assert pycron.is_now('* * 1,16,18 * *', now)
    assert pycron.is_now('* * 19 * *', now) is False
    assert pycron.is_now('* * */4 * *', now) is False
    assert pycron.is_now('* * 1,16 * *', now) is False
