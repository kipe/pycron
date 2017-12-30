from datetime import datetime
from nose.tools import assert_raises
import pycron


def test_minutes():
    since = datetime(2015, 6, 18, 0, 1)
    now = datetime(2015, 6, 18, 0, 3)

    assert pycron.has_been('* * * * *', since, now)
    assert pycron.has_been('0 * * * *', since, now) is False
    assert pycron.has_been('1 * * * *', since, now)
    assert pycron.has_been('2 * * * *', since, now)
    assert pycron.has_been('3 * * * *', since, now)
    assert pycron.has_been('4 * * * *', since, now) is False


def test_hours():
    since = datetime(2015, 6, 18, 1, 0)
    now = datetime(2015, 6, 18, 3, 0)

    assert pycron.has_been('* * * * *', since, now)
    assert pycron.has_been('* 0 * * *', since, now) is False
    assert pycron.has_been('* 1 * * *', since, now)
    assert pycron.has_been('* 2 * * *', since, now)
    assert pycron.has_been('* 3 * * *', since, now)
    assert pycron.has_been('* 4 * * *', since, now) is False


def test_days():
    since = datetime(2015, 6, 1, 0, 0)
    now = datetime(2015, 6, 3, 0, 0)

    assert pycron.has_been('* * * * *', since, now)
    assert pycron.has_been('* * 0 * *', since, now) is False
    assert pycron.has_been('* * 1 * *', since, now)
    assert pycron.has_been('* * 2 * *', since, now)
    assert pycron.has_been('* * 3 * *', since, now)
    assert pycron.has_been('* * 4 * *', since, now) is False


def test_raises():
    since = datetime(2016, 6, 1, 0, 0)
    now = datetime(2015, 6, 3, 0, 0)
    assert_raises(ValueError, pycron.has_been, '* * * * *', since, now)