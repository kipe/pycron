from datetime import datetime
import pycron


def test_parser():
    now = datetime(2015, 6, 18, 16, 7)
    try:
        pycron.is_now('* *,2 * * *', now)
        assert False
    except ValueError:
        assert True

    try:
        pycron.is_now('* 1/2 * * *', now)
        assert False
    except ValueError:
        assert True

    try:
        pycron.is_now('* /2 * * *', now)
        assert False
    except ValueError:
        assert True

    try:
        pycron.is_now('* , * * *', now)
        assert False
    except ValueError:
        assert True
