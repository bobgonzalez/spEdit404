from note import Note


def create_dumb_note(**kwargs):
    return Note(pad=kwargs.get('pad', 1), bank=kwargs.get('bank', 'a'),
                start_tick=kwargs.get('start_tick', 0), length=kwargs.get('length', 60),
                velocity=kwargs.get('velocity', 127))