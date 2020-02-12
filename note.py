import constants


class Note:
    def __init__(self, pad, bank, start_tick, length, velocity):
        pad = int(pad)
        start_tick = int(start_tick)
        length = int(length)
        velocity = int(velocity)

        if 0 < pad <= constants.pads_per_bank and type(start_tick) == int:
            self.pad = pad
        else:
            raise ValueError(f'pad must be integer between 1-{constants.pads_per_bank}')
        if 0 <= ord(bank.lower())-constants.ascii_character_offset < 8:
            self.bank = bank.lower()
        else:
            raise ValueError('bank must be a letter between a-h')
        if start_tick >= 0 and type(start_tick) == int:
            self.start_tick = start_tick
        else:
            raise ValueError('start_tick must be a positive integer')
        if length >= 0 and type(length) == int:
            self.length = length
        else:
            raise ValueError('length must be a positive integer')
        self.end_tick = self.start_tick + self.length
        if 0 < velocity <= constants.max_velocity and type(start_tick) == int:
            self.velocity = velocity
        else:
            raise ValueError(f'velocity must be integer between 1-{constants.max_velocity}')

    def __eq__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        return (self.pad == other.pad
                and self.bank == other.bank
                and self.start_tick == other.start_tick
                and self.length == other.length
                and self.velocity == other.velocity)

    def __str__(self):
        return f"{self.bank}{self.pad}"