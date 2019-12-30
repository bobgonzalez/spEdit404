from track import Pattern, Note
from binary_utilities import read_pattern, write_binary
from wave import preview_pattern
from utils import create_folder


def menu():
    return input("r : read pattern from binary\n" + "a : add note\n" + "d : delete note\n" + "l : set pattern length\n"
                 + "w : write pattern to binary\n" + "p : preview pattern\n" + "x : exit\n>")


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
    length = input('enter length of pattern or enter \'r\' to load pattern >')
    if length == 'r':
        bank, pad = get_user_input(['bank', 'pad'])
        pattern = read_pattern(bank, pad)
    else:
        pattern = Pattern(int(length))
    while True:
        print(pattern)
        menu_choice = menu()
        if menu_choice == 'a':
            bank, pad, velocity, length, start_tick = get_user_input(['bank', 'pad', 'velocity 0-127',
                                                                      'length', f'note start 0-{384 * len(pattern)}> '])
            new_note = Note(pad, bank, start_tick, length, velocity)
            pattern.add_note(new_note)
        elif menu_choice == 'w':
            bank, pad = get_user_input(['bank', 'pad'])
            write_binary(pattern, bank, pad)
        elif menu_choice == 'r':
            bank, pad = get_user_input(['bank', 'pad'])
            pattern = read_pattern(bank, pad)
        elif menu_choice == 'l':
            pattern.change_length = int(input('enter number of bars > '))
        elif menu_choice == 'd':
            track, note = get_user_input(['track', 'note'])
            pattern.delete_note(track, note)
        elif menu_choice == 'p':
            bpm = get_user_input(['bpm'])
            preview_pattern(pattern, bpm)
        elif menu_choice == 'x':
            break
