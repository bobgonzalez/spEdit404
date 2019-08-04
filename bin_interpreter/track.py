import copy


class Pattern:
    def __init__(self, length):
        self.length = int(length)
        self.notes = []

    def __add__(self, other):
        new_pattern = Pattern2(len(self)+len(other))
        notes_to_add = copy.deepcopy(other.notes)
        for note in notes_to_add:
            note.time_start = note.time_start + (self.length*384)
        new_pattern.notes = sorted(self.notes+other.notes, key=lambda note: note.time_start)
        return new_pattern

    def __len__(self):
        return self.length

    def add_note(self, note):
        self.notes.append(note)
        self.notes = sorted(self.notes, key=lambda note: note.time_start)

    def delete_note(self, note_index):
        self.notes.pop(note_index)


class Note:
    def __init__(self, pad, bank, start_tick, length, velocity):
        self.pad = pad
        self.bank = bank
        self.start_tick = start_tick
        self.length = length
        self.velocity = velocity