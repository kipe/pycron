from datetime import datetime
import mock
from nose.tools import raises


def test_minute():
    now = datetime(2015, 6, 18, 16, 7)
    assert mock.is_now(now, '* * * * *')
    assert mock.is_now(now, '* 16 * * *')
    assert mock.is_now(now, '* */4 * * *')
    assert mock.is_now(now, '*/7 16 * * *')
    assert mock.is_now(now, '*/7 */8 * * *')
    assert mock.is_now(now, '* */9 * * *') is False
    assert mock.is_now(now, '* */5 * * *') is False
    assert mock.is_now(now, '*/3 */4 * * *') is False
    assert mock.is_now(now, '3 16 * * *') is False
    assert mock.is_now(now, '*/8 */3 * * *') is False


@raises(ValueError)
def test_value_error():
    now = datetime(2015, 6, 18, 0, 9)
    mock.is_now(now, '* */13 * * *')
