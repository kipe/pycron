from datetime import datetime
import mock
import pycron


def test_parser():
    now = datetime(2015, 6, 18, 16, 7)
    assert mock.is_now(now, '* * * * *')
    assert mock.is_now(now, '* * * * 3')
    assert mock.is_now(now, '* * * * */3')
    assert mock.is_now(now, '* * * * 0,3,4')
    assert mock.is_now(now, '* * * * 4') is False
    assert mock.is_now(now, '* * * * */2') is False
    assert mock.is_now(now, '* * * * 0,4,6') is False
    assert pycron.DOW_CHOICES[1][now.isoweekday()] == 'Thursday'
    assert pycron.DOW_CHOICES[1][7] == 'Sunday'
