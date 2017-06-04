class Note():
    def __init__(self, b, p, v, le, n, s):
        if b != 0:
            self.time_start = s
            self.time_end = s + le
            self.pad = p
            self.bank = b.lower()
            self.bank_switch = 0
            self.pad_code = self.calc_pad_code(b, p)
            self.velocity = v
            self.length = le
            self.next_note = n
            self.teenth = self.time_start / 24
        else:
            self.time_start = s
            self.time_end = 60
            self.pad = 0
            self.bank = 0
            self.bank_switch = 0
            self.pad_code = str(hex(128))[2:]
            self.velocity = 127
            self.length = 60
            self.next_note = n

    def set_length(self, le):
        length = str(hex(le))[2:]
        if len(length) == 1:
            length = '00 0' + str(length)
        elif len(length) == 2:
            length = '00 ' + str(length)
        elif len(length) == 3:
            length = '0' + str(length)[:1] + ' ' + str(length)[1:]
        elif len(length) == 4:
            length = str(length)[:2] + ' ' + str(length)[2:]
        return length

    def calc_pad_code(self, b, p):
        ascii_bank = ord(b.lower())
        ascii_bank -= 97
        if ascii_bank > 4:
            self.bank_switch = 1
            ascii_bank -= 5
        ascii_bank *= 12
        offset = ascii_bank + int(p) + 46
        return str(hex(offset))[2:]

    def write(self):
        #FIX EROR WHEN WRITING NOTE WHOSE HEX NEXT NOTE VALUE IS 3 DIGIT, NEEDS POST NOTE PADDING
        v = str(hex(self.velocity))[2:]
        if len(v) == 1:
            v = '0' + v
        if len(str(hex(self.next_note))[2:]) == 1:
            n = '0' + str(self.next_note)
        else:
            n = str(hex(self.next_note))[2:]
        encoding = n + ' ' + str(self.pad_code) + ' 0' + str(self.bank_switch) + ' 00 ' + v + ' 40 ' + self.set_length(self.length)
        return encoding

    def gen_pad_bank(self):
        real_code = int(self.pad_code, 16) - 46
        bank = real_code / 12
        pad = real_code % 12
        if pad == 0:
            pad = 12
            bank -= 1
        if self.bank_switch == 1:
            bank += 5
        ascii_bank = chr(bank + 97)
        self.bank = ascii_bank
        self.pad = pad

    def set_next_note(self, n):
        self.next_note = n
