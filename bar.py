from note import *

'''
Bars should be start padded with an empty note
Bars last notes nextnote value should not extend past end of bar, use start padding
'''


class Bar():
    def __init__(self):
        self.table = []
        self.time = 0
        for i in range(12):
            self.table.append(
                ['[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]',
                 '[   ]', '[   ]', '[   ]', '[   ]', '[   ]'])
        self.table.append(
            ['0/16 ', '1/16 ', '2/16 ', '3/16 ', '4/16 ', '5/16 ', '6/16 ', '7/16 ', '8/16 ', '9/16 ', '10/16', '11/16',
             '12/16', '13/16', '14/16', '15/16'])
        self.notes = []
        #self.notes.append(Note(0, 0, 0, 0, 60, 384))

    def add_note(self, note, index):
        note.time = self.time
        note.time_end = note.time + note.length
        self.time += int(note.next_note)
        self.notes.insert(index, note)

    def add_note2(self, note, index):
        if len(self.notes) == 0:
            self.add_note(Note(0, 0, 0, 0, index*24, 0), 0)
        self.notes[len(self.notes)-1].next_note = index*24 - self.notes[len(self.notes)-1].time
        note.next_note = 384 - note.time
        note.time_end = note.time + note.length
        self.time = 384
        self.notes.insert(len(self.notes), note)

    def add_note_at(self, note, index):
        time = 0
        note.time = index * 24
        note.time_end = note.time + int(note.length)
        if note.time > self.time or len(self.notes) == 0:
            self.add_note2(note, index)
            return
        for i, inote in enumerate(self.notes):
            time += int(inote.next_note)
            if index * 24 == time:
                note.next_note = 0
                self.notes.insert(i + 1, note)
                return
            elif index * 24 < time:
                self.notes[i].next_note = (index * 24) - (time - inote.next_note)
                note.next_note = time - (index * 24)
                self.notes.insert(i + 1, note)
                return

    def delete_note(self, bank, pad, index):
        #NEED TO FIX IF NOTE TO BE DELETED IS THE FIRST IN THE BAR
        for i in range(len(self.notes)):
            if self.notes[i].time < (index + 1) * 24 and self.notes[i].time >= index * 24:
                if self.notes[i].bank == bank and self.notes[i].pad == int(pad):
                    self.notes[i-1].next_note += self.notes[i].next_note
                    pnotes = self.notes[:i] + self.notes[i+1:]
                    self.notes = pnotes
                    break

    def change_note_velocity(self, bank, pad, index, velocity):
        for i in range(len(self.notes)):
            if self.notes[i].time < (index + 1) * 24 and self.notes[i].time >= index * 24:
                if self.notes[i].bank == bank and self.notes[i].pad == int(pad):
                    self.notes[i].velocity = velocity
                    break

    def change_note_length(self, bank, pad, index, length):
        for i in range(len(self.notes)):
            if self.notes[i].time < (index + 1) * 24 and self.notes[i].time >= index * 24:
                if self.notes[i].bank == bank and self.notes[i].pad == int(pad):
                    self.notes[i].length = length
                    self.notes[i].time_end = self.notes[i].time_start + length
                    break

    def print_pattern(self):
        self.table = []
        table = ''
        current_time = 0
        current_note = 0
        for i in range(12):
            self.table.append(
                ['[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]', '[   ]',
                 '[   ]', '[   ]', '[   ]', '[   ]', '[   ]'])
        self.table.append(
            ['0/16 ', '1/16 ', '2/16 ', '3/16 ', '4/16 ', '5/16 ', '6/16 ', '7/16 ', '8/16 ', '9/16 ', '10/16', '11/16',
             '12/16', '13/16', '14/16', '15/16'])
        for i in range(16):
            while current_time < (i+1) * 24:
                if current_note == len(self.notes):
                    break
                note = self.notes[current_note]
                if str(note.bank) != '0':
                    self.insert_into((str(note.bank) + str(note.pad)), i, note.time_end)
                current_time += note.next_note
                current_note += 1
        for i in range(13):
            num = str(12-i) + ' '
            if len(num) == 2:
                num = ' ' + num
            if num == ' 0 ':
                num = '   '
            table += num + ' '.join(self.table[i])
            table += '\n'
        return table

    def insert_into(self, n, k, e):
        first = True
        for i in range(12):
            row = True
            for j in range(16-k):
                if e > 24 * (i+j):
                    if self.table[11-i][k+j] != '[   ]':
                        row = False
            if row:
                for j in range(16 - k):
                    if e > 24 * (k+j):
                        if first:
                            if len(n) == 2:
                                n += ' '
                            first = False
                            self.table[11 - i][k+j] = '[' + n + ']'
                        else:
                            self.table[11 - i][k + j] = '.....'
                return
