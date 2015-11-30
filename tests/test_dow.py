from datetime import datetime
import pycron


def test_parser():
    now = datetime(2015, 6, 18, 16, 7)
    assert pycron.is_now('* * * * *', now)
    assert pycron.is_now('* * * * 4', now)
    assert pycron.is_now('* * * * */4', now)
    assert pycron.is_now('* * * * 0,3,4', now)
    assert pycron.is_now('* * * * 3', now) is False
    assert pycron.is_now('* * * * */3', now) is False
    assert pycron.is_now('* * * * 0,3,6', now) is False
    assert pycron.DOW_CHOICES[now.isoweekday()][1] == 'Thursday'
    assert pycron.DOW_CHOICES[0][1] == 'Sunday'

    now = datetime(2015, 6, 21, 16, 7)
    assert pycron.is_now('* * * * 0', now)
