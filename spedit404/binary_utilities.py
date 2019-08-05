import binascii
from itertools import islice
from spedit404 import constants
from spedit404.track import Pattern, Note


def write_binary(pattern, bank_letter, pad_number):
    outputBIN = f'./export/PTN00{get_pad_code(bank_letter, pad_number)}.BIN'
    pattern_length_encoding = f'00 8C 00 00 00 00 00 00 \n00 {get_bar_code(pattern)} 00 00 00 00 00 00'
    if os.path.exists('./test.txt'):
        os.remove('./test.txt')
    buffer_file = open('./test.txt', 'w+')
    for i, note in enumerate(pattern.notes):
        buffer_file.write(write_note(note, pattern.notes[i+1].start_tick))
    buffer_file.write(str(pattern_length_encoding))
    buffer_file.close()
    with open('test.txt') as f, open(outputBIN, 'wb') as output_binary:
        for line in f:
            output_binary.write(
                binascii.unhexlify(''.join(line.split()))
            )
    f.close()
    output_binary.close()


def write_note(note, next_note_start_tick):
    #  TODO FIX EROR WHEN WRITING NOTE WHOSE HEX NEXT NOTE VALUE IS 3 DIGIT, NEEDS POST NOTE PADDING
    velocity = add_padding(str(hex(note.velocity))[2:], 2)
    next_note = note.start_tick - next_note_start_tick
    if len(str(hex(next_note))[2:]) == 1:
        next_note = '0' + str(next_note)
    else:
        next_note = str(hex(next_note))[2:]
    pad_code, bank_switch = gen_pad_code_bank_switch(note.bank, note.pad)
    encoding = next_note + ' ' + pad_code + ' 0' + bank_switch + ' 00 ' + velocity + ' 40 ' + \
               get_hex_length(note.length) + '\n'
    return encoding


def gen_pad_code_bank_switch(bank_letter, pad_number):
    bank_number = ord(bank_letter.lower()) - constants.ascii_character_offset
    bank_switch = 1 if bank_number > constants.number_of_bank_pads else 0
    bank_number -= constants.secondary_bank_offset if bank_switch else 0
    bank_offset = bank_number * constants.pads_per_bank
    pad_offset = bank_offset + int(pad_number) + constants.pad_offset_magic_number
    return str(hex(pad_offset))[2:], str(bank_switch)


def get_hex_length(length):
    length = str(hex(length))[2:]
    length = zero_pad(length)
    return length


def zero_pad(paddee):
    if len(paddee) == 1:
        length = '00 0' + str(paddee)
    elif len(paddee) == 2:
        length = '00 ' + str(paddee)
    elif len(paddee) == 3:
        length = '0' + str(paddee)[:1] + ' ' + str(paddee)[1:]
    elif len(paddee) == 4:
        length = str(paddee)[:2] + ' ' + str(paddee)[2:]
    return length

def add_padding(padee, length):
    while len(padee) < length:
        padee = '0' + padee
    return padee


def get_bar_code(pattern):
    if len(pattern) < 16:
        return '0' + str(hex(pattern.length))[2:]
    return str(hex(pattern.length))[2:]


def get_pad_code(bank_letter, pad_number):
    bank = ord(bank_letter.lower()) - 97
    code = str(hex((bank * 12) + int(pad_number)))[2:]
    return add_padding(code, 3)


def gen_pad_bank(pad_code, bank_switch):
    real_code = int(pad_code, 16) - constants.pad_offset_magic_number
    bank = int(real_code / 12)
    pad = real_code % 12
    if pad == 0:
        pad = 12
        bank -= 1
    if bank_switch == 1:
        bank += 5
    ascii_bank = chr(bank + constants.ascii_character_offset)
    pd = str(pad)
    if len(pd) == 1:
        pd = "0" + pd
    return pd, ascii_bank.upper()


def read_pattern(bank_letter, pad_number):
    inputBIN = f'./import/PTN00{get_pad_code(bank_letter, pad_number)}.BIN'
    with open(inputBIN, 'rb') as f:
        hexdata = binascii.hexlify(f.read())
    split_list = list(chunk(hexdata, 16))
    sl = []
    for i, l in enumerate(split_list):
        sl.append(list(chr(i) for i in l))
    #    for j, asci in enumerate(l):
    #        split_list[i][j] == chr(asci)
    note_list = sl[:-2]
    pattern = Pattern(int(str(sl[-1][2] + sl[-1][3]), base=16))

    current_time = 0
    for i, note in enumerate(note_list):
        if str(note[2] + note[3]) != '80' or len(pattern.notes) == 0:
            ticks_till_next_note = int(str(note[0] + note[1]), 16)
            velocity = int(str(note[8] + note[9]), 16)
            length_ticks = int(str(note[12] + note[13] + note[14] + note[15]), 16)
            pad, bank = gen_pad_bank(pad_code=str(note[2] + note[3]), bank_switch=note[5])
            pattern.add_note(Note(bank=bank, pad=pad, velocity=velocity, length=length_ticks, start_tick=current_time))
            current_time += ticks_till_next_note
    return pattern


def chunk(data, size):
    data = iter(data)
    return iter(lambda: tuple(islice(data, size)), ())