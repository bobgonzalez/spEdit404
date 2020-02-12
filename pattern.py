import copy
import os

import constants
from track import Track
from utils import add_padding

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

    def delete_all_tracks(self):
        self.tracks = [Track(self.length) for i in range(NUMBER_OF_TRACKS)]

    def delete_all_occurrences_of_note(self, bank, pad):
        for track in self.tracks:
            track.delete_all_occurrences_of_note(bank, pad)