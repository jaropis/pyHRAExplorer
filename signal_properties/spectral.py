from my_exceptions import WrongSignal
import scipy
import scipy.signal as scisignal

class LombScargleSpectrum:
    def __init__(self, signal):
        self.filtered_signal, self.filtered_time_track = self.filter_and_timetrack(signal)
        self.periodogram, self.frequency = self.build_spectrum()

    def filter_and_timetrack(self, signal):
        # this function prepares data for Lomb-Scargle - i.e. filtered cumulative sum of time,   filtered signal
        bad_beats = scipy.where(signal.annotation != 0)[0]
        filtered_timetrack = scipy.delete(signal.timetrack, bad_beats)
        filtered_signal = scipy.delete(signal.signal, bad_beats)
        return filtered_signal, filtered_timetrack

    def build_spectrum(self):
        frequency = scipy.linspace(0.01, 2*scipy.pi, len(self.filtered_time_track)) # here the asumption is that the frequenices are below 1Hz
        # which obviously may not be true
        periodogram = scisignal.lombscargle(self.filtered_time_track, self.filtered_signal, frequency) / len(self.filtered_time_track) * 4 * self.filtered_time_track[len(self.filtered_time_track)-1] / (2*scipy.pi) / 2
        return periodogram, frequency
