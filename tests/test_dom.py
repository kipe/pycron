from datetime import datetime
import mock


def test_parser():
    now = datetime(2015, 6, 18, 16, 7)
    assert mock.is_now(now, '* * * * *')
    assert mock.is_now(now, '* * 18 * *')
    assert mock.is_now(now, '* * */6 * *')
    assert mock.is_now(now, '* * 1,16,18 * *')
    assert mock.is_now(now, '* * 19 * *') is False
    assert mock.is_now(now, '* * */4 * *') is False
    assert mock.is_now(now, '* * 1,16 * *') is False
