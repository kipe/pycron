from datetime import datetime
import mock
from nose.tools import raises


def test_minute():
    now = datetime(2015, 6, 18, 0, 9)
    assert mock.is_now(now, '* * * * *')
    assert mock.is_now(now, '9 * * * *')
    assert mock.is_now(now, '*/1 * * * *')
    assert mock.is_now(now, '*/3 * * * *')
    assert mock.is_now(now, '*/9 * * * *')
    assert mock.is_now(now, '*/2 * * * *') is False
    assert mock.is_now(now, '*/4 * * * *') is False
    assert mock.is_now(now, '*/5 * * * *') is False
    assert mock.is_now(now, '*/12 * * * *') is False
    assert mock.is_now(now, '*/12 * * * *') is False


@raises(ValueError)
def test_value_error():
    now = datetime(2015, 6, 18, 0, 9)
    mock.is_now(now, '*/31 * * * *')
