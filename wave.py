import constants
from utils import add_padding

from pydub import AudioSegment
from pydub.playback import play


def preview_pattern(pattern, bpm):
    bpm = int(bpm)
    MpT = milliseconds_per_tick(bpm)
    pattern_audio = AudioSegment.silent(duration=constants.ticks_per_bar * pattern.length * MpT)
    for track in pattern.tracks:
        for note in track.notes:
            pd = add_padding(str(note.pad), 2)
            path = f"{constants.path_to_samples}{note.bank.upper()}00000{pd}.WAV"
            sample_audio = AudioSegment.from_file(path)
            pattern_audio = pattern_audio.overlay(sample_audio[:note.length * MpT], position=note.start_tick)
    play(pattern_audio)


def milliseconds_per_tick(bpm):
    return ((constants.millisec_per_min/bpm)/constants.ticks_per_bar)*4
