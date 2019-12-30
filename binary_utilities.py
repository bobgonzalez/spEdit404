import constants
from track import Pattern, Note
from utils import remove_file, add_padding

import binascii
from itertools import islice


def write_binary(pattern, bank_letter, pad_number):
    outputBIN = f'./export/PTN00{get_pad_code(bank_letter, pad_number)}.BIN'
    pattern_length_encoding = f'00 8C 00 00 00 00 00 00 \n00 {get_bar_code(pattern)} 00 00 00 00 00 00'
    remove_file('./test.txt')
    with open(outputBIN, 'wb') as output_binary:
        notes = []
        for track in pattern.tracks:
            notes += track.notes
        notes = sorted(notes, key=lambda note: note.start_tick)
        for i, note in enumerate(notes):
            next_note_start = 0 if i+1 == len(notes) else notes[i+1].start_tick
            write_hex(output_binary, write_note(note, next_note_start))
        write_hex(output_binary, pattern_length_encoding)


def write_hex(out_file, hex):
    out_file.write(binascii.unhexlify(''.join(hex.split())))


def write_note(note, next_note_start_tick):
    #  TODO FIX EROR WHEN WRITING NOTE WHOSE HEX NEXT NOTE VALUE IS 3 DIGIT, NEEDS POST NOTE PADDING
    velocity = add_padding(str(hex(note.velocity))[2:], 2)
    next_note = note.start_tick - next_note_start_tick
    if len(str(hex(next_note))[2:]) == 1:
        next_note = '0' + str(next_note)
    else:
        next_note = str(hex(next_note))[2:]
    pad_code, bank_switch = gen_pad_code_bank_switch(note.bank, note.pad)
    encoding = f'{next_note}{pad_code}0{bank_switch}00{velocity}40{get_hex_length(note.length)}\n'
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
    length = add_padding(length, 4)
    return length


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
    pd = add_padding(str(pad), 2)
    return pad, ascii_bank.upper()


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