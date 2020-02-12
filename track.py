import constants

import copy
import math

FRAMES_PER_BAR = 16
RESOLUTION = int(constants.TICKS_PER_BAR / FRAMES_PER_BAR)


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

    def delete_all_occurrences_of_note(self, bank, pad):
        self.notes = list(filter(lambda note: note.bank != bank.lower() and note.pad != int(pad), self.notes))

    def notes_collide(self, new_note, note):
        return ((note.start_tick <= new_note.start_tick <= note.end_tick)
                or (note.start_tick <= new_note.end_tick <= note.end_tick)
                or (new_note.start_tick <= note.end_tick <= new_note.end_tick)
                or (new_note.start_tick <= note.end_tick <= new_note.end_tick))
