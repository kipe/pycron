from datetime import datetime
import mock
import pycron


def test_parser():
    now = datetime(2015, 6, 18, 16, 7)
    assert mock.is_now(now, '* * * * *')
    assert mock.is_now(now, '* * * 6 *')
    assert mock.is_now(now, '* * * */2 *')
    assert mock.is_now(now, '* * * 1,4,6,12 *')
    assert mock.is_now(now, '* * * 5 *') is False
    assert mock.is_now(now, '* * * */5 *') is False
    assert mock.is_now(now, '* * * 1,4,12 *') is False
    assert pycron.MONTH_CHOICES[now.month - 1][1] == 'June'
