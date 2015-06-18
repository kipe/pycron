from datetime import datetime
import mock


def test_parser():
    now = datetime(2015, 6, 18, 16, 7)
    try:
        mock.is_now(now, '* *,2 * * *')
        assert False
    except ValueError:
        assert True

    try:
        mock.is_now(now, '* 1/2 * * *')
        assert False
    except ValueError:
        assert True

    try:
        mock.is_now(now, '* /2 * * *')
        assert False
    except ValueError:
        assert True

    try:
        mock.is_now(now, '* , * * *')
        assert False
    except ValueError:
        assert True
