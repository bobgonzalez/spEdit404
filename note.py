from pydub import AudioSegment
import constants
from timer import Timer


class Note():
    def __init__(self, bank, pad, velocity, length, next, start, timer=Timer(95)):
        if bank != 0:
            self.timer = timer
            self.time_start = start
            self.time_end = start + length
            self.pad = pad
            self.bank = bank.lower()
            self.bank_switch = 0
            self.pad_code = self.calculate_pad_code(bank, pad)
            self.velocity = velocity
            self.length = length
            self.next_note = next
            self.teenth = self.time_start / 24
            pd = str(self.pad)
            if len(pd) == 1:
                pd = "0" + pd
            self.path = "/home/robert/PycharmProjects/spEdit404/SP-404SX/SMPL/" + self.bank.upper() + \
                        "00000" + pd + ".WAV"
            print(self.path)
            silence = AudioSegment.from_file("/home/robert/PycharmProjects/spEdit404/silence.wav")
            s1 = silence[:self.timer.milli_per_tick]
            start = s1 * self.time_start
            self.audio = start + AudioSegment.from_file(self.path)[:self.length * self.timer.milli_per_tick]
            #self.audio.export("/home/robert/PycharmProjects/spEdit404/mixed.wav", format='wav')
        else:
            self.audio = AudioSegment.silent(duration=10000)
            self.time_start = start
            self.time_end = 60
            self.pad = 0
            self.bank = 0
            self.bank_switch = 0
            self.pad_code = str(hex(128))[2:]
            self.velocity = 127
            self.length = 60
            self.next_note = next

    def get_hex_length(self, length):
        length = str(hex(length))[2:]
        length = self.zero_pad(length)
        return length

    def set_bpm(self, timer):
        self.timer = timer

    def zero_pad(self, length):
        if len(length) == 1:
            length = '00 0' + str(length)
        elif len(length) == 2:
            length = '00 ' + str(length)
        elif len(length) == 3:
            length = '0' + str(length)[:1] + ' ' + str(length)[1:]
        elif len(length) == 4:
            length = str(length)[:2] + ' ' + str(length)[2:]
        return length

    def calculate_pad_code(self, bank_letter, pad_number):
        ascii_bank = ord(bank_letter.lower())
        bank_number = ascii_bank - constants.ascii_character_offset
        if bank_number > constants.number_of_bank_pads:
            self.bank_switch = 1
            bank_number -= constants.secondary_bank_offset
        bank_offset = bank_number * constants.pads_per_bank
        pad_offset = bank_offset + int(pad_number) + constants.pad_offset_magic_number
        return str(hex(pad_offset))[2:]

    def write(self):
        #  TODO FIX EROR WHEN WRITING NOTE WHOSE HEX NEXT NOTE VALUE IS 3 DIGIT, NEEDS POST NOTE PADDING
        v = str(hex(self.velocity))[2:]
        if len(v) == 1:
            v = '0' + v
        if len(str(hex(self.next_note))[2:]) == 1:
            n = '0' + str(self.next_note)
        else:
            n = str(hex(self.next_note))[2:]
        encoding = n + ' ' + str(self.pad_code) + ' 0' + str(self.bank_switch) + ' 00 ' + v + ' 40 ' + \
                   self.get_hex_length(self.length)
        return encoding

    def gen_pad_bank(self):
        real_code = int(self.pad_code, 16) - constants.pad_offset_magic_number
        bank = int(real_code / 12)
        pad = real_code % 12
        if pad == 0:
            pad = 12
            bank -= 1
        if self.bank_switch == 1:
            bank += 5
        ascii_bank = chr(bank + constants.ascii_character_offset)
        self.bank = ascii_bank
        self.pad = pad
        pd = str(self.pad)
        if len(pd) == 1:
            pd = "0" + pd
        self.path = "/home/robert/PycharmProjects/spEdit404/SP-404SX/SMPL/" + self.bank.upper() + "00000" + pd + ".WAV"
        print(self.path)
        silence = AudioSegment.from_file("/home/robert/PycharmProjects/spEdit404/silence.wav")
        s1 = silence[:self.timer.milli_per_tick]
        s = s1 * self.time_start
        self.audio = s + AudioSegment.from_file(self.path)[:self.length * self.timer.milli_per_tick]

    def set_next_note(self, next):
        self.next_note = next
