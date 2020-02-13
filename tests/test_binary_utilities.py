import unittest

from binary_utilities import read_pattern, write_pattern
from pattern import Pattern


class TestBinaryUtilities(unittest.TestCase):
    # TODO test note collision when new note starts or ends in existing note
    # TODO test note collision when existing note starts or ends in new note

    def set_up(self):
        self.pattern = Pattern(1)
        self.binary = ''

    def test_reading_pattern(self):
        pass
