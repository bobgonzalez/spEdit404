import constants
from utils import add_padding

import copy
import math
import os


FRAMES_PER_BAR = 16
RESOLUTION = int(constants.TICKS_PER_BAR / FRAMES_PER_BAR)
NUMBER_OF_TRACKS = 12


class Pattern:
    def __init__(self, length):
        self.length = int(length)
        self.tracks = [Track(length) for i in range(NUMBER_OF_TRACKS)]

    def __add__(self, other):
        new_pattern = copy.deepcopy(self)
        new_pattern.change_length(len(self) + len(other))
        notes_to_add = copy.deepcopy(other.notes)
        for note in notes_to_add:
            note.time_start = note.time_start + (self.length * constants.TICKS_PER_BAR)
            new_pattern.add_note(note)
        return new_pattern

    def __len__(self):
        return self.length

    def __str__(self):
        ret = ''
        for bar in range(len(self)):
            ret += f'Bar#{bar}{os.linesep}'
            for i, track in enumerate(self.tracks):
                ret += f'{add_padding(i, 2)}:\t{track.print_bar(bar)}{os.linesep}'
        return ret

    def add_note(self, new_note):
        if new_note.start_tick < self.length*constants.TICKS_PER_BAR:
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
        track_index = int(track_index)
        note_index = int(note_index)
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
            note.time_start = note.time_start + (self.length * constants.TICKS_PER_BAR)
            new_track.add_note(note)
        return new_track

    def __len__(self):
        return self.length

    def print_bar(self, bar_number):
        #  The following var's assume that bar_number is 0 indexed
        bar_start = 384*bar_number
        bar_end = 384*(bar_number+1)

        bar = ['..' for i in range(FRAMES_PER_BAR)]
        for note in self.notes:
            if bar_start <= note.start_tick < bar_end:
                #  print note in the earliest frame that it appears
                start_frame = math.floor(note.start_tick / RESOLUTION) % 16
                #  print note playing till the latest frame that it plays in
                end_frame = math.ceil(note.end_tick / RESOLUTION)
                if end_frame > FRAMES_PER_BAR:
                    end_frame = FRAMES_PER_BAR
                bar[start_frame] = str(note)
                if end_frame != start_frame:
                    bar[start_frame+1:end_frame] = ['--' for i in range(end_frame-(start_frame+1))]
            elif bar_start <= note.end_tick <= bar_end:
                end_frame = math.ceil(note.end_tick / RESOLUTION) % 16
                if end_frame == 0:
                    end_frame = 16
                bar[:end_frame] = ['--' for i in range(end_frame)]
            elif note.start_tick < bar_start and note.end_tick > bar_end:
                bar = ['--' for i in range(FRAMES_PER_BAR)]
        return bar



    def add_note(self, new_note):
        if new_note.start_tick < self.length*constants.TICKS_PER_BAR:
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
                or (note.start_tick <= new_note.end_tick <= note.end_tick)
                or (new_note.start_tick <= note.end_tick <= new_note.end_tick)
                or (new_note.start_tick <= note.end_tick <= new_note.end_tick))


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
        return f"{self.bank}{self.pad}"
