import unittest

from binary_utilities import read_pattern, write_pattern
from pattern import Pattern
from tests.test_utils import create_dumb_note
from unittest.mock import patch, mock_open


class TestBinaryUtilities(unittest.TestCase):
    # TODO test note collision when new note starts or ends in existing note
    # TODO test note collision when existing note starts or ends in new note

    def set_up(self):
        self.pattern = Pattern(1)
        self.pattern.add_note(create_dumb_note())
        self.binary = b'1101010100'

    def test_reading_pattern(self):
        self.set_up()
        with patch("builtins.open", mock_open(read_data=self.binary)) as mock_file:
            read_pattern('a', 1)
            mock_file.assert_called_with('./import/PTN00001.BIN', 'rb')

    def test_writing_pattern(self):
        self.set_up()
        with patch("builtins.open", mock_open(read_data=self.binary)) as mock_file:
            write_pattern(self.pattern, 'a', 1)
            mock_file.assert_called_with('./export/PTN00001.BIN', 'wb')
