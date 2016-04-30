from my_exceptions import WrongCuts
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

    def get_bands(self, cuts):
        self.test_cuts(cuts)
        # cuts is a list holding the frequency bands of interest
        first = cuts[0]
        power_in_bands = []
        for second in cuts[1:]:
            # no interpolation since the frequencies are closely spaced in self.frequency (see the build_spectrum method)
            first_index = scipy.where(self.frequency <= first)[0]
            second_index = scipy.where(self.frequency <= second)[0]
            if len(second_index > 0):
                power_in_bands.append(sum(self.periodogram[first_index[-1]:second_index[-1]]))
                first = second
            elif first_index[0] < len(self.periodogram):
                power_in_bands.append(sum(self.periodogram[first_index[-1]:len(self.periodogram)]))
                break
            else:
                break
        return power_in_bands

    def test_cuts(self, cuts):
        if len(cuts) != len(scipy.unique(cuts)) or (cuts != sorted(cuts)):
            raise WrongCuts
