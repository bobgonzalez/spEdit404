import unittest
from bin_interpreter import track

class TestTrack(unittest.TestCase):

    def __init__(self):
        self.pattern = track.Pattern(1)

    def test_cant_create_note_out_of_velocity_bounds(self):
        pass

    def test_cant_create_note_out_of_bank_bounds(self):
        pass

    def test_cant_create_note_out_of_pad_bounds(self):
        pass

    def test_cant_create_note_negative_start(self):
        pass

    def test_cant_create_note_negative_length(self):
        pass

    def test_pattern_add_note(self):
        pass

    def test_cant_add_note_start_past_pattern_length(self):
        pass

    def test_cant_add_note_length_past_pattern_length(self):
        pass

    def test_cant_add_note_causing_13_tracks(self):
        pass

    def create_dumb_note(self, **kwargs):
        return track.Note(pad=kwargs.get('pad', 1), bank=kwargs.get('bank', 'a'),
                          start_tick=kwargs.get('start_tick', 0), length=kwargs.get('length', 60),
                          velocity=kwargs.get('velocity', 127))

if __name__ == '__main__':
    unittest.main()