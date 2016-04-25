from my_exceptions import WrongSignal
import scipy

class LombScargleSpectrum:
    def __init__(self, signal):
        self.filtered_signal, self.filtered_time_track = self.filter_and_timetrack(signal)

    def filter_and_timetrack(self, signal):
        # this function prepares data for Lomb-Scargle - i.e. filtered cumulative sum of time,   filtered signal
        bad_beats = scipy.where(signal.annotation != 0)[0]
        filtered_timetrack = scipy.delete(signal.timetrack, bad_beats)
        filtered_signal = scipy.delete(signal.signal, bad_beats)

        return filtered_signal, filtered_timetrack





