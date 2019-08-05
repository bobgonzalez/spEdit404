from pydub import AudioSegment
from pydub.playback import play
from spedit404 import constants


def preview_pattern(pattern, bpm):
    MpT = milliseconds_per_tick(bpm)
    pattern_audio = AudioSegment.silent(duration=constants.ticks_per_bar * pattern.length * MpT)
    for note in pattern.notes:
        pd = str(note.pad)
        if len(pd) == 1:
            pd = "0" + pd
        path = "./SP-404SX/SMPL/" + note.bank.upper() + "00000" + pd + ".WAV"
        sample_audio = AudioSegment.from_file(path)
        pattern_audio = pattern_audio.overlay(sample_audio[:note.length * MpT], position=note.start_tick)
    play(pattern_audio)


def milliseconds_per_tick(bpm):
    return ((constants.millisec_per_min/bpm)/constants.ticks_per_bar)*4
