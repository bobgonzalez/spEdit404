import unittest
from track import Note, Pattern


class TestTrack(unittest.TestCase):

    def set_up(self):
        self.pattern = Pattern(1)

    def test_cant_create_note_out_of_velocity_bounds(self):
        self.assertRaises(ValueError, Note, 1, 'a', 0, 60, 128)
        self.assertRaises(ValueError, Note, 1, 'a', 0, 60, -1)

    def test_cant_create_note_out_of_bank_bounds(self):
        self.assertRaises(ValueError, Note, 1, 'i', 0, 60, 10)

    def test_cant_create_note_out_of_pad_bounds(self):
        self.assertRaises(ValueError, Note, -1, 'a', 0, 60, 10)
        self.assertRaises(ValueError, Note, 13, 'a', 0, 60, 10)

    def test_cant_create_note_negative_start(self):
        self.assertRaises(ValueError, Note, 1, 'a', -10, 60, 10)

    def test_cant_create_note_negative_length(self):
        self.assertRaises(ValueError, Note, 1, 'a', 10, -60, 10)

    def test_pattern_add_note(self):
        self.set_up()
        self.pattern.add_note(self.create_dumb_note())
        self.assertEquals(self.pattern.notes[0], self.create_dumb_note())

    def test_cant_add_note_start_past_pattern_length(self):
        pass

    def test_cant_add_note_length_past_pattern_length(self):
        pass

    def test_cant_add_note_causing_13_tracks(self):
        pass

    def create_dumb_note(self, **kwargs):
        return Note(pad=kwargs.get('pad', 1), bank=kwargs.get('bank', 'a'),
                          start_tick=kwargs.get('start_tick', 0), length=kwargs.get('length', 60),
                          velocity=kwargs.get('velocity', 127))

if __name__ == '__main__':
    unittest.main()