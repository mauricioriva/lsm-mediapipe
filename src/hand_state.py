from enum import Enum


class HandState(Enum):
    open = 'open'
    close = 'close'
    mid = 'mid'

    def __str__(self):
        return self.value

    @staticmethod
    def from_string(s):
        try:
            return HandState[s]
        except KeyError:
            raise ValueError()
