from pattern import Pattern
from tests.test_utils import create_dumb_note
import unittest


class TestNote(unittest.TestCase):

    def set_up(self):
        pass

    def test_create_dumb_note(self):
        create_dumb_note()

    def test_cant_create_note_out_of_velocity_bounds(self):
        self.assertRaises(ValueError, create_dumb_note, velocity=128)
        self.assertRaises(ValueError, create_dumb_note, velocity=-1)

    def test_cant_create_note_out_of_bank_bounds(self):
        self.assertRaises(ValueError, create_dumb_note, bank='i')

    def test_cant_create_note_out_of_pad_bounds(self):
        self.assertRaises(ValueError, create_dumb_note, pad=-1)
        self.assertRaises(ValueError, create_dumb_note, pad=13)

    def test_cant_create_note_negative_start(self):
        self.assertRaises(ValueError, create_dumb_note, start_tick=-1)

    def test_cant_create_note_negative_length(self):
        self.assertRaises(ValueError, create_dumb_note, length=-1)


class TestPattern(unittest.TestCase):
    # TODO test setting and changing pattern length out of bounds 0<x<99
    # TODO test note collision when new note starts or ends in existing note
    # TODO test note collision when existing note starts or ends in new note
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


if __name__ == '__main__':
    unittest.main()
