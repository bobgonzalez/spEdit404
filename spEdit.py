from pattern import Pattern
from note import Note
from binary_utilities import read_pattern, write_pattern
from wave import preview_pattern
from utils import create_folder

import sys


def menu():
    print(*[f'{k}: {v.__name__}' for k, v in action_map.items()], sep='\n')
    return input('>')


def setup_folders():
    folders = ["./export", "./import", "./tmp"]
    [create_folder(folder) for folder in folders]


def get_user_input(fields):
    values = []
    [values.append(input(f'enter {field} > ')) for field in fields]
    return values


def play_pattern(pattern):
    bpm = input(f'enter bpm > ')
    preview_pattern(pattern, bpm)
    return pattern


def delete_note_from_pattern(pattern):
    track, note = get_user_input(['track', 'note'])
    pattern.delete_note(track, note)
    return pattern


def delete_note_occurrences_from_pattern(pattern):
    bank, pad = get_user_input(['bank', 'pad'])
    pattern.delete_all_occurrences_of_note(bank, pad)
    return pattern


def delete_all_notes_from_pattern(pattern):
    pattern.delete_all_tracks()
    return pattern


def change_pattern_length(pattern):
    pattern.change_length = int(input('enter number of bars > '))
    return pattern


def read_pattern_from_file(pattern):
    bank, pad = get_user_input(['bank', 'pad'])
    pattern = read_pattern(bank, pad)
    return pattern


def write_pattern_to_file(pattern):
    bank, pad = get_user_input(['bank', 'pad'])
    write_pattern(pattern, bank, pad)
    return pattern


def add_note_to_pattern(pattern):
    bank, pad, velocity, length, start_tick = get_user_input(['bank', 'pad', 'velocity 0-127',
                                                              'length', f'note start 0-{384 * len(pattern)}> '])
    try:
        new_note = Note(pad, bank, start_tick, length, velocity)
        pattern.add_note(new_note)
    except ValueError as e:
        print(f'\n{e}\n')
    return pattern


def exit(pattern):
    sys.exit()


action_map = {
    'r': read_pattern_from_file,
    'a': add_note_to_pattern,
    'w': write_pattern_to_file,
    'l': change_pattern_length,
    'd': delete_note_from_pattern,
    'dn': delete_note_occurrences_from_pattern,
    'da': delete_all_notes_from_pattern,
    'p': play_pattern,
    'x': exit,
}

if __name__ == "__main__":
    setup_folders()
    menu_choice = input('enter length of pattern or enter \'r\' to load pattern >')
    if menu_choice == 'r':
        bank, pad = get_user_input(['bank', 'pad'])
        pattern = read_pattern(bank, pad)
    else:
        pattern = Pattern(int(menu_choice))
    while menu_choice != 'x':
        print(pattern)
        menu_choice = menu()
        pattern = action_map[menu_choice](pattern)
