import unittest
import pycron


class RandomTestCase(unittest.TestCase):
    def test_parse_arg(self):
        assert pycron._parse_arg("1/5", 0) is False
        assert pycron._parse_arg("asd-dsa", 0) is False

    def test_no_dt(self):
        assert pycron.is_now("* * * * *")
