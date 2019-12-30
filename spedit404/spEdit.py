from track import Pattern, Note
from binary_utilities import read_pattern, write_binary
from wave import *
from utils import create_folder


def menu():
    ret = ("r : read pattern from binary\n" + "a : add note\n" + "d : delete note\n"
           + "l : set pattern length\n" + "w : write pattern to binary\n" + "x : exit\n")
    return ret


def setup_folders():
    create_folder("./export")
    create_folder("./import")
    create_folder("./tmp")


def get_user_input(fields):
    values = []
    for field in fields:
        values.append(input(f'enter {field} > '))
    return values


if __name__ == "__main__":
    setup_folders()
    length = input('enter length of pattern in bars or enter \'r\' to load pattern >')
    if length != 'r':
        length = int(length)
        pattern = Pattern(length)
    else:
        bank, pad = get_user_input(['bank', 'pad'])
        pattern = read_pattern(bank, pad)
        print(pattern)
    while True:
        print(menu())
        usr_in = input('> ')
        if usr_in == 'a':
            bank, pad, velocity, length, start_tick = get_user_input(['bank', 'pad', 'velocity 0-127',
                                                                      'length', f'note start 0-{384 * len(pattern)}> '])
            new_note = Note(pad, bank, start_tick, length, velocity)
            pattern.add_note(new_note)
            print(pattern)
        elif usr_in == 'pr':
            print(pattern)
        elif usr_in == 'w':
            bank, pad = get_user_input(['bank', 'pad'])
            write_binary(pattern, bank, pad)
        elif usr_in == 'r':
            bank, pad = get_user_input(['bank', 'pad'])
            pattern = read_pattern(bank, pad)
            print(pattern)
        elif usr_in == 'l':
            pattern.change_length = int(input('enter number of bars > '))
            print(pattern)
        elif usr_in == 'd':
            track = input('enter track # 0-11 > ')
            note = input('enter note # 0-n > ')
            pattern.delete_note(track, note)
            print(pattern)
        elif usr_in == 'x':
            break
