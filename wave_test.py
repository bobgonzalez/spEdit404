import wave
import math
import struct
import contextlib
from pydub import AudioSegment
from pydub.silence import split_on_silence
from os import *
#from pyaudio import *


def duration():
    """"-------------------------------------------------------------------------------------------"""
    fname = './tmp/test.wav'
    #fname = f_name
    with contextlib.closing(wave.open(fname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        d = frames / float(rate)
        return d


def create_wave_sample():
    """"-------------------------------------------------------------------------------------------"""
    FILENAME = "./tmp/test.wav"
    freq = 440.0
    data_size = 40000
    frate = 1000.0
    amp = 64000.0
    nchannels = 2
    sampwidth = 2
    framerate = int(frate)
    nframes = data_size
    comptype = "NONE"
    compname = "not compressed"
    data = [(math.sin(2 * math.pi * freq * (x / frate)),
            math.cos(2 * math.pi * freq * (x / frate))) for x in range(data_size)]
    try:
        wav_file = wave.open(FILENAME, 'w')
        wav_file.setparams(
            (nchannels, sampwidth, framerate, nframes, comptype, compname))
        for values in data:
            for v in values:
                wav_file.writeframes(struct.pack('h', int(v * amp / 2)))
    finally:
        wav_file.close()


def mixer():
    """"-------------------------------------------------------------------------------------------"""
    audio1 = AudioSegment.from_file("chunk1.wav") #your first audio file
    audio2 = AudioSegment.from_file("chunk2.wav") #your second audio file
    audio3 = AudioSegment.from_file("chunk3.wav") #your third audio file

    mixed = audio1.overlay(audio2)          #combine , superimpose audio files
    mixed1  = mixed.overlay(audio3)          #Further combine , superimpose audio files
    #If you need to save mixed file
    mixed1.export("mixed.wav", format='wav') #export mixed  audio file
    mixed1.play()                             #play mixed audio file
    # pydub does things in miliseconds
    ten_seconds = 10 * 1000
    first_10_seconds = mixed1[:10000]
    mixed_loop = mixed1 * 2
    # ticks to millisecond conversion using bpm
    # create silence multiply by number of ticks till sample then add them and overlay


def preview_pat(pat):
    """"-------------------------------------------------------------------------------------------"""
    silence = AudioSegment.from_file("/home/robert/PycharmProjects/spEdit404/silence.wav")
    s1 = silence[:pat.MpT]
    ret = s1[:1]
    for bar in pat.score:
        for note in bar.notes:
            print("here")
            print(note.path)
            s = s1 * note.time_start
            a = AudioSegment.from_file(note.path)
            ret.overlay(s+a[:note.length*pat.MpT])
    ret.play()


def split_on_silence():
    """"-------------------------------------------------------------------------------------------"""
    #sound = AudioSegment.from_mp3("my_file.mp3")
    sound = AudioSegment.from_wav('./tmp/test.wav')
    chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=-16)
        # must be silent for at least half a second
        # consider it silent if quieter than -16 dBFS
    if os.path.isdir("./tmp/test"):
        for file in listdir("./tmp/test"):
            remove("./tmp/test/" + file)
    elif os.path.isdir("./tmp"):
        os.mkdir("./tmp/test")
    else:
        os.mkdir("./tmp")
        os.mkdir("./tmp/test")
    for i, chunk in enumerate(chunks):
        chunk.export("./tmp/test/chunk{0}.wav".format(i), format="wav")
