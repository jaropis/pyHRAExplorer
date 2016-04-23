from my_exceptions import WrongSignal


class Runs:
    def __init__(self, signal):
        self.filtered_signal, self.time_track = self.filter_and_timetrack(signal)

    def filter_and_timetrack(self, signal):
        pass
