from pydub import AudioSegment
from bin_interpreter import constants


def preview_pattern(pattern, bpm):
    MpT = milliseconds_per_tick(bpm)
    silence = AudioSegment.from_file("./silence.wav")
    s1 = silence[:MpT]
    ret = s1[:1]
    for bar in pattern.score:
        for note in bar.notes:
            print(note.path)
            s = s1 * note.start_tick
            pd = str(note.pad)
            if len(pd) == 1:
                pd = "0" + pd
            path = "./SP-404SX/SMPL/" + note.bank.upper() + "00000" + pd + ".WAV"
            a = AudioSegment.from_file(path)
            ret.overlay(s + a[:note.length * MpT])
    ret.play()


def milliseconds_per_tick(bpm):
    return ((constants.millisec_per_min/bpm)/constants.ticks_per_bar)*4
