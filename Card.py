class Card(object):
    def __init__(self, number, is_specical_card=False):
        self._number = number

    @property
    def number(self):
        return self._number

    def __repr__(self):
        return str(self.number)