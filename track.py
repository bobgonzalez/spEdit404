import copy
from . import constants

class Pattern:
    def __init__(self, length):
        self.length = int(length)
        self.notes = []

    def __add__(self, other):
        new_pattern = Pattern(len(self)+len(other))
        notes_to_add = copy.deepcopy(other.notes)
        for note in notes_to_add:
            note.time_start = note.time_start + (self.length*constants.ticks_per_bar)
        new_pattern.notes = sorted(self.notes+other.notes, key=lambda n: n.time_start)
        return new_pattern

    def __len__(self):
        return self.length

    def add_note(self, note):
        if note.start_tick < self.length*constants.ticks_per_bar:
            self.notes.append(note)
            self.notes = sorted(self.notes, key=lambda note: note.time_start)
        else:
            raise ValueError('note must start before the pattern ends')

    def delete_note(self, note_index):
        self.notes.pop(note_index)


class Note:
    def __init__(self, pad, bank, start_tick, length, velocity):
        if 0 < pad <= constants.pads_per_bank and type(start_tick) == int:
            self.pad = pad
        else:
            raise ValueError(f'pad must be integer between 1-{constants.pads_per_bank}')
        if 0 < ord(bank.lower())-constants.ascii_character_offset < 9:
            self.bank = bank
        else:
            raise ValueError('bank must be a letter between a-h')
        if start_tick >= 0 and type(start_tick) == int:
            self.start_tick = start_tick
        else:
            raise ValueError('start_tick must be a positive integer')
        if length >= 0 and type(length) == int:
            self.length = length
        else:
            raise ValueError('length must be a positive integer')
        if 0 < velocity <= constants.max_velocity and type(start_tick) == int:
            self.velocity = velocity
        else:
            raise ValueError(f'velocity must be integer between 1-{constants.max_velocity}')
