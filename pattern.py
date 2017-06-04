import binascii
from itertools import islice
from bar import *
import copy
import os

class Pattern():
    def __init__(self, length):
        self.length = int(length)
        self.time = 0
        self.ticks = length * 384
        self.score = []
        for i in range(length):
            self.score.append(Bar())

    def double(self):
        for i in range(self.length):
            b = copy.deepcopy(self.score[i])
            self.score.append(b)
        self.length *= 2

    def change_note_velocity(self, bank, pad, bar, index, velocity):
        self.score[bar - 1].change_note_velocity(bank, pad, index, velocity)

    def change_note_length(self, bank, pad, bar, index, length):
        self.score[bar - 1].change_note_length(bank, pad, index, length)

    def add_note(self, note, bar, index):
        self.score[bar].add_note(note, index)

    def delete_note(self, bank, pad, bar, index):
        self.score[bar-1].delete_note(bank, pad, index)

    def add_note_at(self, note, bar, index):
        self.score[bar].add_note_at(note, index)

    def clear_notes(self):
        self.score = []
        for j in range(self.length):
                self.score.append(Bar())

    def print_pattern(self):
        table = ''
        for i in range(self.length):
            table += 'Bar #' + str(i + 1) + '\n'
            table += self.score[i].print_pattern()
        return table

    def read_pattern(self, b, p):
        bank = ord(b.lower())
        bank -= 97
        code = str(hex((bank*12)+int(p)))[2:]
        if len(code) == 2:
            code = '0' + code
        elif len(code) == 1:
            code = '00' + code
        inputBIN = './import/PTN00'+ code +'.BIN'
        self.time = 0
        with open(inputBIN, 'rb') as f:
            hexdata = binascii.hexlify(f.read())
        #hexlist = map(''.join, zip(hexdata[::2], hexdata[1::2]))
        split_list = list(self.chunk(hexdata, 16))
        note_list = split_list[:-2]
        self.length = int(str(split_list[-1][2] + split_list[-1][3]), 16)
        self.score = []
        for i in range(self.length):
            self.score.append(Bar())
        ctime = 0
        miss = 0
        bar = 0
        for i, note in enumerate(note_list):
            if str(note[2] + note[3]) != '80' or len(self.score[bar].notes) == 0:
                nn = int(str(note[0] + note[1]), 16)
                v = int(str(note[8] + note[9]), 16)
                le = int(str(note[12] + note[13] + note[14] + note[15]), 16)
                n = Note('a', 1, v, le, nn, ctime)
                n.pad_code = str(note[2] + note[3])
                n.bank_switch = note[5]
                n.gen_pad_bank()
                ctime += n.next_note
                self.score[bar].add_note(n, i-miss)
            else:
                if i > 0:
                    self.score[bar].notes[i-1].next_note += int(str(note[0] + note[1]), 16)
                else:
                    self.score[bar-1].notes[len(self.score[bar-1].notes)-1].next_note += int(str(note[0] + note[1]), 16)
                miss += 1
                ctime += int(str(note[0] + note[1]), 16)
            if ctime >= 384:
                bar += 1
                ctime -= 384

    def chunk(self, it, size):
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

    def write_binary(self, b, p):
        bank = ord(b.lower())
        bank -= 97
        code = str(hex((bank * 12) + int(p)))[2:]
        if len(code) == 2:
            code = '0' + code
        elif len(code) == 1:
            code = '00' + code
        outputBIN = './export/PTN00' + code + '.BIN'
        if self.length < 16:
            bars = '0' + str(hex(self.length))[2:]
        else:
            bars = str(hex(self.length))[2:]
        end_encoding = '00 8C 00 00 00 00 00 00 \n00 ' + str(bars) + ' 00 00 00 00 00 00'
        if os.path.exists('./test.txt'):
            os.remove('./test.txt')
        f1 = open('./test.txt', 'w+')
        for bar in self.score:
            for note in bar.notes:
                f1.write(note.write())
                f1.write('\n')
        f1.write(end_encoding)
        f1.close()
        with open('test.txt') as f, open(outputBIN, 'wb') as fout:
            for line in f:
                fout.write(
                    binascii.unhexlify(''.join(line.split()))
                )
        f.close()
        fout.close()
