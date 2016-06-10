from signal_properties.my_exceptions import WrongCuts
import scipy
import scipy.signal as scisignal

class LombScargleSpectrum:
    def __init__(self, signal):
        self.filtered_signal, self.filtered_time_track = self.filter_and_timetrack(signal)
        self.periodogram, self.frequency = self.build_spectrum()
        #self.bands = self.get_bands(cuts=[0, 0.003, 0.04, 0.15, 0.4], df=self.frequency[1]-self.frequency[0]) # this
        # is basically the result which is expected in HRV - depending on the length of the recording the first two
        # entries may be combined to VLF in short recordings

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

    def get_bands(self, cuts, df):
        self.test_cuts(cuts)
        # cuts is a list holding the frequency bands of interest
        # df is the integration measure
        first = cuts[0]
        power_in_bands = []
        for second in cuts[1:]:
            # no interpolation since the frequencies are closely spaced in self.frequency (see the build_spectrum method)
            first_index = scipy.where(self.frequency >= first)[0]
            second_index = scipy.where(self.frequency >= second)[0]
            print(first_index, second_index, self.frequency[0])
            if first_index[0] == second_index[0]: ## here, if there is no power in the first band, and there is some in the following one, this condition must hold
                power_in_bands.append(0.0)
                first = second # go to the next band
            elif len(second_index > 0): # if there is any power in the band above the current band
                power_in_bands.append(sum(self.periodogram[first_index[-1]:second_index[0]]))
                first = second
            elif len(first_index) >= 1: # so, there is no power in the band above - is there any power
                power_in_bands.append(sum(self.periodogram[first_index[0]:first_index[-1]]))
                break
            else:
                break
        return scipy.array(power_in_bands) * df

    def test_cuts(self, cuts):
        if len(cuts) != len(scipy.unique(cuts)) or (cuts != sorted(cuts)):
            raise WrongCuts
