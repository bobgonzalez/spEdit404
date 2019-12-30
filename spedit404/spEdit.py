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



if __name__ == "__main__": 
    setup_folders()
    length = input('enter length of pattern in bars or enter \'r\' to load pattern >')
    if length != 'r':
        length = int(length)
        p = Pattern(length)
    else:
        bank = input('enter bank > ')
        pad = input('enter pad > ')
        try:
            p = read_pattern(bank, pad)
        except Exception as e:
            e.printStackTrace()
            print("error reading binary : error 202")
        print(p)
    while True:
        print(menu())
        usr_in = input('> ')
        try:
            if usr_in == 'a':
                b = input('enter bank > ')
                pad = int(input('enter pad # > '))
                v = int(input('enter velocity 0-127 > '))
                le = int(input('enter length > '))
                n = int(input(f'enter note start 0-{384*len(p)}> '))
                try:
                    n4 = Note(pad, b, n, le, v)
                except Exception as e:
                    e.printStackTrace()
                    print("error creating note : 101")
                try:
                    p.add_note(n4)
                except Exception as e:
                    e.printStackTrace()
                    print("error adding note : error 301")
                print(p)
            elif usr_in == 'pr':
                print(p)
            elif usr_in == 'w':
                bank = input('enter bank > ')
                pad = input('enter pad > ')
                try:
                    write_binary(p, bank, pad)
                except Exception as e:
                    e.printStackTrace()
                    print("error writing binary : error 203")
            elif usr_in == 'r':
                bank = input('enter bank > ')
                pad = input('enter pad > ')
                try:
                    p = read_pattern(bank, pad)
                    print(p)
                except Exception as e:
                    e.printStackTrace()
                    print("error reading binary : error 202")
            elif usr_in == 'l':
                p.change_length = int(input('enter number of bars > '))
                print(p)
            elif usr_in == 'd':
                track = input('enter track # 0-11 > ')
                note = input('enter note # 0-n > ')
                try:
                    p.delete_note(track, note)
                except Exception as e:
                    e.printStackTrace()
                    print("error deleting note : error 305")
                print(p)
            elif usr_in == 'x':
                break
        except Exception as e:
            e.printStackTrace()
            print("error reading input : error 201")
