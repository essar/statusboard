class SRFlipFlop:
    def __init__(self):
        self.set = 0
        self.reset = 0
        self.output = 0

    def clock(self):
        self.output = 0 if self.reset == 1 else self.set

    @property
    def set(self):
        return self.__set

    @set.setter
    def set(self, _set):
        self.__set = _set

    @property
    def reset(self):
        return self.__reset

    @reset.setter
    def reset(self, _reset):
        self.__reset = _reset
