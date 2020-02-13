import unittest

from tests.test_utils import create_dumb_note


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