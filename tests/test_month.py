from datetime import datetime
import pycron


def test_parser():
    now = datetime(2015, 6, 18, 16, 7)
    assert pycron.is_now('* * * * *', now)
    assert pycron.is_now('* * * 6 *', now)
    assert pycron.is_now('* * * */2 *', now)
    assert pycron.is_now('* * * 1,4,6,12 *', now)
    assert pycron.is_now('* * * 5 *', now) is False
    assert pycron.is_now('* * * */5 *', now) is False
    assert pycron.is_now('* * * 1,4,12 *', now) is False
    assert pycron.MONTH_CHOICES[now.month - 1][1] == 'June'
