import constants
from pattern import Pattern
from note import Note
from utils import add_padding

import binascii
from itertools import islice


def write_pattern(pattern, bank_letter, pad_number):
    output_binary_path = f'./export/PTN00{get_pad_code(bank_letter, pad_number)}.BIN'
    with open(output_binary_path, 'wb') as output_binary:
        notes = get_sorted_notes(pattern)
        for i, note in enumerate(notes):
            write_note_hex_data(i, note, notes, output_binary)
        write_pattern_length_hex_data(output_binary, pattern)


def get_sorted_notes(pattern):
    notes = [note for track in pattern.tracks for note in track.notes]
    notes = sorted(notes, key=lambda n: n.start_tick)
    return notes


def write_note_hex_data(i, note, notes, output_binary):
    is_last_note = i + 1 == len(notes)
    next_note_start = note.start_tick if is_last_note else notes[i + 1].start_tick
    write_hex(output_binary, write_note(note, next_note_start))


def write_pattern_length_hex_data(output_binary, pattern):
    pattern_length_encoding = constants.length_encoding.format(get_bar_code(pattern))
    write_hex(output_binary, pattern_length_encoding)


def write_hex(out_file, hex_string):
    out_file.write(binascii.unhexlify(''.join(hex_string.split()).strip()))


def write_note(note, next_note_start_tick):
    #  TODO FIX ERROR WHEN WRITING NOTE WHOSE HEX NEXT NOTE VALUE IS 3 DIGIT, NEEDS POST NOTE PADDING
    velocity = add_padding(str(hex(note.velocity))[2:], 2)
    next_note = next_note_start_tick - note.start_tick
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
    bank = ord(bank_letter.lower()) - constants.ascii_character_offset
    code = str(hex((bank * constants.pads_per_bank) + int(pad_number)))[2:]
    return add_padding(code, 3)


def gen_pad_bank(pad_code, bank_switch):
    real_code = int(pad_code, 16) - constants.pad_offset_magic_number
    bank = int(real_code / constants.pads_per_bank)
    pad = real_code % constants.pads_per_bank
    if pad == 0:
        pad = 12
        bank -= 1
    if bank_switch == 1:
        bank += 5
    ascii_bank = chr(bank + constants.ascii_character_offset)
    return pad, ascii_bank.upper()


def read_pattern(bank_letter, pad_number):
    hex_data = get_hex_character_row_representation(bank_letter, pad_number)
    note_list = hex_data[:-2]
    pattern_length = int(str(hex_data[-1][2] + hex_data[-1][3]), base=16)
    pattern = Pattern(pattern_length)

    current_time = 0
    for chunk_index, note in enumerate(note_list):
        #if str(note[2] + note[3]) != '80' or len(pattern.notes) == 0:
        if str(note[2] + note[3]) != '80':
            ticks_till_next_note = int(str(note[0] + note[1]), 16)
            velocity = int(str(note[8] + note[9]), 16)
            length_ticks = int(str(note[12] + note[13] + note[14] + note[15]), 16)
            pad, bank = gen_pad_bank(pad_code=str(note[2] + note[3]), bank_switch=note[5])
            pattern.add_note(Note(bank=bank, pad=pad, velocity=velocity, length=length_ticks, start_tick=current_time))
            current_time += ticks_till_next_note
    return pattern


def get_hex_character_row_representation(bank_letter, pad_number):
    # this reads in the binary data as one hex byte string
    raw_hex_data = get_pattern_hex_data(bank_letter, pad_number)
    # this breaks the hex into 16 byte chunks
    # inadvertently casting the bytes as integer representations of ascii characters
    integer_data_chunks = list(chunk(raw_hex_data, 16))
    # this converts the integer representations to ascii characters
    hex_data = [(list(chr(integer_byte) for integer_byte in integer_data_chunk))
                for integer_data_chunk in integer_data_chunks]
    return hex_data


def get_pattern_hex_data(bank_letter, pad_number):
    input_binary_path = f'./import/PTN00{get_pad_code(bank_letter, pad_number)}.BIN'
    with open(input_binary_path, 'rb') as input_binary:
        hex_data = binascii.hexlify(input_binary.read())
    return hex_data


def chunk(data, size):
    data = iter(data)
    return iter(lambda: tuple(islice(data, size)), ())
