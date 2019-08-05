from spedit404 import constants


class Timer():

    def __init__(self, bpm):
        self.bpm = bpm
        self.milli_per_tick = ((constants.millisec_per_min / self.bpm) / constants.ticks_per_bar) * 4
