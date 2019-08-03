from pattern import *
from wave_test import *
from note import *

import wave
import math
import struct
import contextlib
from pydub import AudioSegment
from pydub.silence import split_on_silence
from os import *
import subprocess

'''
TODO: use redis or shelve to let user save patterns
TODO: e - edit hex values
TODO: V - change all velocities
TODO: D* - delete all occurrences of one pad, V* - change all velocities of one pad
TODO: add swing function
TODO: add triplet function
TODO: move note by ticks
TODO: copy subsection of pattern
TODO: merge two patterns
TODO: REFACTOR
TODO: add more try, except blocks to prevent crash on wrong input
TODO 404 to midi
'''


def menu():
    ret = "r : read pattern from binary\n" + "i : insert note\n" + "d : delete note\nD : clear all notes\n" + "v : change note velocities\n" + "h : change note length\n" + "l : set pattern length\n" + "m : double pattern\n" + "w : write pattern to binary\n" + "x : exit\n"
    return ret


def preview_pat(pat):
    """"-------------------------------------------------------------------------------------------"""
    ret = AudioSegment.silent(duration=pat.MpT*384*pat.length*4)
    for i, bar in enumerate(pat.score):
        silence = AudioSegment.silent(duration=pat.MpT * 384 * i * 4)
        #s1 = silence[:pat.MpT]
        #s = s1 * self.time_start
        for note in bar.notes:
            #print("here")
            #print(note.path)
            #s = s1 * note.time_start
            #a = AudioSegment.from_file(note.path)
            ret = ret.overlay(silence + note.audio)
            #print("here")
    ret.export("/home/robert/PycharmProjects/spEdit404/mixed.wav", format='wav')
    subprocess.call(["ffplay", "-nodisp", "-autoexit", "/home/robert/PycharmProjects/spEdit404/mixed.wav"])
   # ret.play()


def setup_folders():
    if not os.path.exists("./export"):
        os.makedirs("./export")
    if not os.path.exists("./import"):
        os.makedirs("./import")
    if not os.path.exists("./tmp"):
        os.makedirs("./tmp")


setup_folders()
length = input('enter length of pattern in bars or enter \'r\' to load pattern >')
if length != 'r':
    length = int(length)
    p = Pattern(length)
else:
    p = Pattern(1)
    bank = input('enter bank > ')
    pad = input('enter pad > ')
    try:
        p.read_pattern(bank, pad)
    except:
        print("error reading binary : error 202")
    print(p.print_pattern())
while True:
    print(menu())
    usr_in = input('> ')
    try:
        if usr_in == 'a':
            b = input('enter bank > ')
            pad = int(input('enter pad # > '))
            v = int(input('enter velocity 0-127 > '))
            le = int(input('enter length > '))
            n = int(input('enter next note start > '))
            try:
                n4 = Note(b, pad, v, le, n, p.time)
            except:
                print("error creating note : 101")
            try:
                p.add_note(n4, len(p.score)-1, len(p.score[len(p.score)-1].notes))
            except:
                print("error adding note : error 301")
        elif usr_in == 'pr':
            print(p.print_pattern())
        elif usr_in == "p":
            print("0 : 1-2-3-4 \n1 : 4 on the floor \n")
            selection = input('enter bank > ')
            if selection == '0':
                for i in range(p.length):
                    n1 = Note('D', 12, 127, 60, 96, 0+(384*i))
                    p.add_note(n1, 0, (4*i)+0)
                    n3 = Note('D', 11, 127, 60, 96, 96+(384*i))
                    p.add_note(n3, 0, (4*i)+1)
                    n2 = Note('D', 9, 127, 60, 96, 192+(384*i))
                    p.add_note(n2, 0, (4*i)+2)
                    n4 = Note('D', 10, 127, 60, 96, 288+(384*i))
                    p.add_note(n4, 0, (4*i)+3)
            elif selection == '1':
                for i in range(p.length * 4):
                    n1 = Note('D', 12, 127, 60, 96, 0+(i*96))
                    p.add_note(n1, 0, 0+i)
            print(p.print_pattern())
        elif usr_in == 'e':
            break
        elif usr_in == 'w':
            bank = input('enter bank > ')
            pad = input('enter pad > ')
            try:
                p.write_binary(bank, pad)
            except:
                print("error writing binary : error 203")
        elif usr_in == 'r':
            bank = input('enter bank > ')
            pad = input('enter pad > ')
            try:
                p.read_pattern(bank, pad)
            except:
                print("error reading binary : error 202")
            print(p.print_pattern())
        elif usr_in == 'l':
            p.length = int(input('enter number of bars > '))
            p.ticks = p.length * 384
            print(p.print_pattern())
        elif usr_in == 'd':
            bank = input('enter bank > ')
            pad = input('enter pad > ')
            bn = int(input('enter bar # > '))
            n = int(input('enter location x : x/16 > '))
            try:
                p.delete_note(bank, pad, bn, n)
            except:
                print("error deleting note : error 305")
            print(p.print_pattern())
        elif usr_in == 'D':
            p.clear_notes()
            print(p.print_pattern())
        elif usr_in == 'v':
            bank = input('enter bank > ')
            pad = input('enter pad > ')
            bn = int(input('enter bar # > '))
            n = int(input('enter location x : x/16 > '))
            v = int(input('enter new velocity 1- 127 > '))
            try:
                p.change_note_velocity(bank, pad, bn, n, v)
            except:
                print("error changing note velocity : error 306")
            print(p.print_pattern())
        elif usr_in == 'i':
            b = input('enter bank > ')
            pad = int(input('enter pad # > '))
            v = int(input('enter velocity 0-127 > '))
            le = int(input('enter length > '))
            bn = int(input('enter bar # > '))
            n = int(input('enter location x : x/16 > '))
            try:
                n4 = Note(b, pad, v, le, n + (bn - 1) * 16, int(n) * 24)
            except:
                print("error creating note : 101")
            try:
                p.add_note_at(n4, bn - 1, n)
            except:
                print("error adding note : error 302")
            print(p.print_pattern())
        elif usr_in == 'm':
            p.double()
            print(p.print_pattern())
        elif usr_in == 'h':
            bank = input('enter bank > ')
            pad = input('enter pad > ')
            bn = int(input('enter bar # > '))
            n = int(input('enter location x : x/16 > '))
            v = int(input('enter new length (384 ticks per bar) > '))
            try:
                p.change_note_length(bank, pad, bn, n, v)
            except:
                print("error changing note length : error 307")
            print(p.print_pattern())
        elif usr_in == 'wt':
            b = input("g : generate wave\n" + "d : calculate duration\n" + "s : split on silence\n" + ' > ')
            if b == 'g':
                create_wave_sample()
            elif b == 'd':
                print(duration())
            elif b == 'p':
                preview_pat(p)
            elif b == 's':
                split_on_silence()
        elif usr_in == 'x':
            break
    except:
        print("error reading input : error 201")
