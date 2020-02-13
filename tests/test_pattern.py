import unittest

from pattern import Pattern
from tests.test_utils import create_dumb_note


class TestPattern(unittest.TestCase):
    # TODO test setting and changing pattern length out of bounds 0<x<99
    # TODO test delete all notes and all occurrences of a note

    def set_up(self):
        self.pattern = Pattern(1)

    def test_pattern_add_note(self):
        self.set_up()
        self.pattern.add_note(create_dumb_note())
        self.assertEqual(self.pattern.tracks[0].notes[0], create_dumb_note())

    def test_cant_add_note_start_past_pattern_length(self):
        self.set_up()
        self.assertRaises(ValueError, self.pattern.add_note, create_dumb_note(start_tick=384))

    @unittest.skip("not sure how SP404-SX handles this need to do more research")
    def test_cant_add_note_length_past_pattern_length(self):
        self.set_up()
        self.assertRaises(ValueError, self.pattern.add_note, create_dumb_note(start_tick=380, length=10))

    def test_cant_add_note_causing_13_tracks(self):
        self.set_up()
        for i in range(13):
            if i == 12:
                self.assertRaises(ValueError, self.pattern.add_note, create_dumb_note())
            else:
                self.pattern.add_note(create_dumb_note())