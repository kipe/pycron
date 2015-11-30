from datetime import datetime
import mock


def test_parser():
    now = datetime(2015, 6, 18, 16, 7)
    assert mock.is_now(now, '* * * * *')
    assert mock.is_now(now, '* 16 * * *')
    assert mock.is_now(now, '* */4 * * *')
    assert mock.is_now(now, '*/7 16 * * *')
    assert mock.is_now(now, '*/7 */8 * * *')
    assert mock.is_now(now, '* 2,8,16 * * *')
    assert mock.is_now(now, '* */9 * * *') is False
    assert mock.is_now(now, '* */5 * * *') is False
    assert mock.is_now(now, '*/3 */4 * * *') is False
    assert mock.is_now(now, '3 16 * * *') is False
    assert mock.is_now(now, '*/8 */3 * * *') is False
    assert mock.is_now(now, '* 2,8 * * *') is False
    assert mock.is_now(now, '* 16-20 * * *')
    assert mock.is_now(now, '* 0-10 * * *') is False
