import unittest

from track import Track
from tests.test_utils import create_dumb_note


class TestTrack(unittest.TestCase):
    # TODO test note collision when new note starts or ends in existing note
    # TODO test note collision when existing note starts or ends in new note

    def set_up(self):
        self.track = Track(1)

    def test_note_collision_1(self):
        pass
