from datetime import datetime, timedelta
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
    assert pycron.is_now('* * * * 0-4', now)
    assert pycron.is_now('* * * * 5-6', now) is False

    now = datetime(2015, 6, 20, 16, 7)
    for i in range(0, 7):
        # Test day matching from Sunday onwards...
        now += timedelta(days=1)
        assert pycron.is_now('* * * * %i' % (i), now)
        # Test weekdays
        assert pycron.is_now('* * * * 1,2,3,4,5', now) is (True if i not in [0, 6] else False)
        # Test weekends
        assert pycron.is_now('* * * * 0,6', now) is (True if i in [0, 6] else False)
