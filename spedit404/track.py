import constants

import copy
import os

class Pattern:
    def __init__(self, length):
        self.length = int(length)
        self.tracks = [Track(length) for i in range(12)]

    def __add__(self, other):
        new_pattern = Pattern(len(self) + len(other))
        notes_to_add = copy.deepcopy(other.notes)
        for note in notes_to_add:
            note.time_start = note.time_start + (self.length*constants.ticks_per_bar)
        new_pattern.notes = sorted(self.notes + other.notes, key=lambda n: n.start_tick)
        return new_pattern

    def __len__(self):
        return self.length

    def __str__(self):
        ret = ''
        for track in self.tracks:
            ret += f'{track}{os.linesep}'
        return ret

    def add_note(self, new_note):
        if new_note.start_tick < self.length*constants.ticks_per_bar:
            for i, track in enumerate(self.tracks):
                try:
                    track.add_note(new_note)
                    return
                except ValueError:
                    pass
            raise ValueError('note can not be added to pattern because it overlaps on all tracks')
        else:
            raise ValueError('note must start before the pattern ends')

    def delete_note(self, track_index, note_index):
        self.tracks[track_index].delete_note(note_index)

    def change_length(self, new_length):
        if 0 < new_length < 99:
            for track in self.tracks:
                track.length = new_length
            self.length = new_length
        raise ValueError('length must be between 1 and 99 bars')


class Track:
    def __init__(self, length):
        self.length = int(length)
        self.notes = []

    def __add__(self, other):
        new_track = Track(len(self)+len(other))
        notes_to_add = copy.deepcopy(other.notes)
        for note in notes_to_add:
            note.time_start = note.time_start + (self.length*constants.ticks_per_bar)
            new_track.add_note(note)
        return new_track

    def __len__(self):
        return self.length

    def __str__(self):
        ret = '..' * int((constants.ticks_per_bar*len(self))/constants.resolution)
        for note in self.notes:
            ret = ret[:int(note.start_tick/constants.resolution)*2] + str(note) + ret[(int(note.end_tick/constants.resolution)+1)*2:]
        return ret

    def add_note(self, new_note):
        if new_note.start_tick < self.length*constants.ticks_per_bar:
            for note in self.notes:
                if self.notes_collide(new_note, note):
                    raise ValueError('notes must not overlap with any notes on track')
            self.notes.append(new_note)
            self.notes = sorted(self.notes, key=lambda note: note.start_tick)
        else:
            raise ValueError('note must start before the pattern ends')

    def delete_note(self, note_index):
        self.notes.pop(note_index)

    def notes_collide(self, new_note, note):
        return ((note.start_tick <= new_note.start_tick <= note.end_tick)
                or (note.start_tick <= new_note.end_tick <= note.end_tick))


class Note:
    def __init__(self, pad, bank, start_tick, length, velocity):
        pad = int(pad)
        start_tick = int(start_tick)
        length = int(length)
        velocity = int(velocity)

        if 0 < pad <= constants.pads_per_bank and type(start_tick) == int:
            self.pad = pad
        else:
            raise ValueError(f'pad must be integer between 1-{constants.pads_per_bank}')
        if 0 <= ord(bank.lower())-constants.ascii_character_offset < 8:
            self.bank = bank.lower()
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
        self.end_tick = self.start_tick + self.length
        if 0 < velocity <= constants.max_velocity and type(start_tick) == int:
            self.velocity = velocity
        else:
            raise ValueError(f'velocity must be integer between 1-{constants.max_velocity}')

    def __eq__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        return (self.pad == other.pad
                and self.bank == other.bank
                and self.start_tick == other.start_tick
                and self.length == other.length
                and self.velocity == other.velocity)

    def __str__(self):
        return f"{self.bank}{self.pad}{'--' * int(self.length/constants.resolution)}"