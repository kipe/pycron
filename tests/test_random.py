import pycron


def test_parse_arg():
    assert pycron._parse_arg('1/5', 0) is False
    assert pycron._parse_arg('asd-dsa', 0) is False


def test_no_dt():
    assert pycron.is_now('* * * * *')
