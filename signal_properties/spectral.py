from signal_properties.my_exceptions import WrongCuts
import numpy as np
import scipy.signal as sc
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd


class LombScargleSpectrum:
    '''
    Class LombAcragleSpectrum used to build periodogram and perform spectral analysis
	
	Attributes:
		filtered_signal (array): An array with the filtered RR signal
	    filtered_timetrack (array): An array with the filtered timetrack
		frequency (array): Array with angular frequecies needed to build the periodogram
        periodogram (array): Array contaning the values of the periodogram, showing which angular frequencies are most common

    '''
    def __init__(self, signal):
        '''
        Initiazes the LombScargleSpectrum

        Args:
	        signal (Signal): Object of class Signal containing signal, annotation and timetrack arrays
        '''
        self.filtered_signal, self.filtered_time_track = self.filter_and_timetrack(signal)
        self.periodogram, self.frequency = self.build_spectrum()
        # self.bands = self.get_bands(cuts=[0, 0.003, 0.04, 0.15, 0.4], df=self.frequency[1]-self.frequency[0]) # this
        # is basically the result which is expected in HRV - depending on the length of the recording the first two
        # entries may be combined to VLF in short recordings

    def filter_and_timetrack(self, signal):
        '''
        This method prepares data for Lomb-Scargle by removing the 'bad beats' and returning filtered data.
        
        Args:
	        signal (Signal): Object of class Signal containing signal, annotation and timetrack arrays
        Returns:
	        filtered_signal (array): An array with the filtered RR signal
	        filtered_timetrack (array): An array with the filtered timetrack
        '''
        # this function prepares data for Lomb-Scargle - i.e. filtered cumulative sum of time,   filtered signal
        bad_beats = np.where(signal.annotation != 0)[0]
        filtered_timetrack = np.delete(signal.timetrack, bad_beats)
        filtered_signal = np.delete(signal.signal, bad_beats)
        return filtered_signal, filtered_timetrack

    def build_spectrum(self):
        '''
        Method for creating a periodogram, showing the periodic behaviour in the time series

        Returns:
            frequency (array): Array with angular frequecies needed to build the periodogram
            periodogram (array): Array contaning the values of the periodogram, showing which angular frequencies are most common
        '''
        frequency = np.linspace(0.01, 2*np.pi, len(self.filtered_time_track))
        # here the assumption is that the frequencies are below 1Hz
        # which obviously may not be true
        periodogram = sc.lombscargle(self.filtered_time_track, self.filtered_signal, frequency) / len(self.filtered_time_track) * 4 * self.filtered_time_track[len(self.filtered_time_track)-1] / (2*np.pi) / 2
        return periodogram, frequency

    def get_bands(self, cuts, df):
        '''
        Method for finsing the total power in bands specified by cuts
        
        Args:
            cuts (list): Holds the frequency bands of interest
            df (int): Integration measure

        Returns:
            bands (array): An array containing total power in each band (bands specified by cuts) multiplied by the integration measure
        '''
        self.test_cuts(cuts)

        first = cuts[0]
        power_in_bands = []
        for second in cuts[1:]:
            # no interpolation since the frequencies are closely spaced in self.frequency (see the build_spectrum method)
            first_index = np.where(self.frequency >= first)[0]
            second_index = np.where(self.frequency >= second)[0]
            # print(first_index, second_index, self.frequency[0])
            if first_index[0] == second_index[0]:
                # here, if there is no power in the first band, and there is some in the following one,
                # this condition must hold
                power_in_bands.append(0.0)
                first = second # go to the next band
            elif len(second_index > 0): # if there is any power in the band above the current band
                power_in_bands.append(sum(self.periodogram[first_index[0]:second_index[0]]))
                first = second
            elif len(first_index) >= 1: # so, there is no power in the band above - is there any power
                power_in_bands.append(sum(self.periodogram[first_index[0]:first_index[-1]]))
                break
            else:
                break
        return (np.array([i * df for i in power_in_bands]), power_in_bands)

    def test_cuts(self, cuts):
        '''
        Method for testing the validity of the cuts argument for the get_bands() method, raises WrongCuts if the cuts are unvalid

        Args:
            cuts (list): Holds the frequency bands of interest
        '''
        if len(cuts) != len(np.unique(cuts)) or (cuts != sorted(cuts)):
            raise WrongCuts
        
    def plot_periodogram(self, mode = 'angular', xlim = [], **kwargs):
        '''
        Method for plotting a periodogram

        Args:
            mode (str): Specifies the mode of the plot, angular (rad/sec) by default but can be changed into Hz, changing the mode changes
            the values and descriptions for the frequency (Hz = rad/sec / 2*pi)
            xlim (list): A list of values which is passed to determine the range of the x axis, full range (0 - 6.28 for rad/sec or 0 - 1 for Hz) shown by default
            **kwargs: key word arguments which can be passed to the matplotlib.pyplots to change the appearance of the plot

        Returns:
            periodogram_plot (Axes): A plot showing the values of the periodogram against the frequency (either rad/sec or Hz)
        '''
        frequency, x_label = (self.frequency/(2*np.pi), 'Frequency [Hz]') if mode == 'Hz' else (self.frequency, 'Angular frequency [rad/s]') 
        fig, periodogram_plot = plt.subplots()
        periodogram_plot.plot(frequency, self.periodogram, **kwargs)
        xlim = plt.xlim() if xlim == [] else xlim
        periodogram_plot.set_xlim(xlim[0], xlim[1])
        periodogram_plot.set_xlabel(x_label)
        periodogram_plot.set_ylabel('Amplitude')

        return periodogram_plot



class WelchSpectrum:
    def __init__(self, signal):
        self.interpolated_rr = self.interpolate_non_sinus(signal)
        #self.test_resample = self.resample_rr(self.interpolated_rr, signal.timetrack)
        self.resampled_timetrack, self.resampled_rr = self.resample_rr(self.interpolated_rr, signal.timetrack)
        self.welch_spectrum = self.calculate_welch(self.resampled_rr)
        self.welch_bands = self.calculate_bands(self.welch_spectrum)

    def interpolate_non_sinus(self, signal):
        """
         this function linearly interpolates the non-sinus beats
        :param rr: the RR intervals time series
        :param flags: the RR intervals annotations
        :return:
        """
        inside_non_sinus = False
        segment_end = 0
        segment_start = 0
        good_segment_start = 0
        good_intervals_list = []
        keep_last = True
        for idx in range(len(signal.signal)):
            if signal.annotation[idx] != 0 and not inside_non_sinus:
                segment_start = idx - 1
                good_intervals_list.append(signal.signal[good_segment_start:(segment_start + 1)])
                inside_non_sinus = True
            if inside_non_sinus and (signal.annotation[idx] == 0  or idx == len(signal.signal) - 1):
                if idx == len(signal.signal) - 1:
                    keep_last = False
                    break
                segment_end = idx
                good_segment_start = segment_end
                interpolated_sequence = self.optimal_division(signal, segment_start, segment_end)
                good_intervals_list.append(interpolated_sequence)
                inside_non_sinus = False
        # now adding the last good segment to good_intervals_list
        if keep_last:
            good_intervals_list.append(signal.signal[good_segment_start:])
        return np.concatenate(good_intervals_list)

    def optimal_division(self, signal, start, stop):
        # the optimal rr interval is to be taken as the mean of the two correct
        # rr intervals surrounding the non-sinus segment
        optimal_rr = (signal.signal[start] + signal.signal[stop])/2
        segment_length = np.cumsum(signal.signal[0:stop])[-1] - np.cumsum(signal.signal[0:start + 1])[-1]
        
        # now searching for optimal division
        optimal = False
        divisions = 1
        delta = np.abs(segment_length - optimal_rr)
        while not optimal:
            current_rr = segment_length / (divisions + 1)
            if np.abs(current_rr - optimal_rr) > delta:
                optimal = True
            else:
                delta = np.abs(current_rr - optimal_rr)
            divisions += 1
        optimal_rr = [segment_length / (divisions - 1)]
        optimal_division = np.array(optimal_rr * (divisions - 1))
        return optimal_division

    def resample_rr(self, signal, timetrack, period = 250, period_type = 'sec', method = 'cubic'):
        """
        this function resamples the RR time series at period - the default value is 250 ms, which corresponds to 0.25 s or 4 Hz
        :rr: the RR intervals time series
        :timetrack: timetrack
        :period: resampling period, default value 250 ms
        :method: interpolation method, default is cubic splines
        """
        if period_type == 'Hz':
            period = 1 / period * 1000
        interp_object = interp1d(np.cumsum(signal), signal, kind=method, fill_value='extrapolate')
        # timetrack is in min, converting period in ms to min
        timetrack_resampled = np.arange(timetrack[0], timetrack[-1], step = period/(60*1000))
        rr_resampled = interp_object(timetrack_resampled)
        return timetrack_resampled, rr_resampled

    def calculate_welch(self, rr_resampled, fs=4, window='hamming', segment_min = 5,
                    noverlap_frac = 0.5):
        """
        function to calculate the actual Welch periodogram
        :param rr_resampled: resampled RR-intervals time series
        :param fs: resampling frequency
        :param window: type of window
        :param segment_min: length of Welch segments in minutes
        :param noverlap_frac: how much to overlap - default is half
        :return: the spectrum in frequency bands
        """
        w_spectrum = sc.welch(rr_resampled - np.mean(rr_resampled), fs=4, window=window, nperseg=segment_min * 60 * fs,
                       noverlap= segment_min * 60 * fs * noverlap_frac, return_onesided=False, scaling='spectrum')

        return w_spectrum

    def calculate_bands(self, w_spectrum, bands=[0.003, 0.04, 0.15, 0.4], ulf=True):
        """
        function to calculate the spectral bands
        :param w_spectrum: Welch spectrum
        :param bands: bands for calculating spectrum
        :param ulf: should I calculate ULF?
        :return: dictionary with band names as keys and spectral bands as values
        """
        #print("pierwsze bandy", bands, bands == [0.003, 0.04, 0.15, 0.4])
        #w_spectrum = list(w_spectrum)
        if not ulf and bands == [0.003, 0.04, 0.15, 0.4]:
            bands = [0.04, 0.15, 0.4]
            band_names = ["vls", "lf", "hf"]
        elif bands == [0.003, 0.04, 0.15, 0.4]:
            band_names = ["ulf", "vlf", "lf", "hf"]
        else:
            band_names = [str(_) for _ in bands]
        #print(bands, band_names)
        extended_bands = [0]; extended_bands.extend(bands)
        spectral_bands = []
        for band_idx in range(1, len(extended_bands)):
            spectral_bands.append(np.sum(np.abs(w_spectrum[1][np.logical_and(w_spectrum[0] > extended_bands[band_idx - 1],
                                                                  w_spectrum[0] <= extended_bands[band_idx])])) * 2)
        spectral_bands.append(np.sum(spectral_bands))
        band_names.append("tp")
        #results = pd.DataFrame([spectral_bands], columns=band_names)
        results = dict(zip(band_names, spectral_bands))

        return results


class FFTSpectrum:
    '''
    Class used to create FFT Spectrum

    Attributes:
        filtered_signal (array): An array with the filtered RR signal
	    filtered_time_track (array): An array with the filtered timetrack
        resampling_rate (): Resampling frequency in Hz
        magnitude (float): magnitude of the fft
        phase (float): phase of the fft
        frequency_axis (float): frequency axis (from minimum to maximum (in the middle, and back)
    '''

    def __init__(self, signal, resampling_rate):
        self.filtered_signal, self.filtered_time_track = FFTSpectrum.filter_and_timetrack(signal)
        self.resampling_rate = resampling_rate # this is the resampling FREQUENCY (in Hz)
        self.magnitude, self.phase, self.frequency = FFTSpectrum.build_fft_spectrum(self.filtered_signal, self.filtered_time_track, self.resampling_rate)
        # self.bands = self.get_bands(cuts=[0, 0.003, 0.04, 0.15, 0.4], df=self.frequency[1]-self.frequency[0]) this
        # is basically the result which is expected in HRV - depending on the length of the recording the first two
        # entries may be combined to VLF in short recordings

    @staticmethod
    def filter_and_timetrack(signal):
        '''
        This method prepares data for Lomb-Scargle and FFT periodograms by removing the 'bad beats' and returning filtered data.
        
        Args:
	        signal (Signal): Object of class Signal containing signal, annotation and timetrack arrays
        Returns:
	        filtered_signal (array): An array with the filtered RR signal
	        filtered_timetrack (array): An array with the filtered timetrack
        '''
        bad_beats = np.where(signal.annotation != 0)[0]
        filtered_timetrack = np.delete(signal.timetrack, bad_beats)
        filtered_signal = np.delete(signal.signal, bad_beats)
        return filtered_signal, filtered_timetrack

    @staticmethod
    def resample(signal, time_track, resampling_rate):
        '''
        This method resamples signal and time_track based on the specified resampling rate

        Args:
            signal (array): The signal after filtering, e.g. RR intervals time series after filtering
            time_track (array): The time track  after filtering, effectively cum summed filtered RR intervals time series
            resampling_rate (float): The rate (in Hz) at which the signal (and the time - track) is to be resampled
        
        Returns:
            signal_resampled (array): An array containg the signal following the resampling
            time_track_resampled (array): An array containg the time_track following the resampling
        '''
        # this method does not use the object in which it is enclosed, so I am making it static
        from np.interpolate import interp1d
        f_interp = interp1d(time_track, signal)
        time_step = 1 / resampling_rate * 1000
        #print(time_step)
        time_track_resampled = np.arange(np.min(time_track), np.max(time_track), step=time_step)
        signal_resampled = f_interp(time_track_resampled)
        return signal_resampled, time_track_resampled

    @staticmethod
    def build_fft_spectrum(signal, time_track, resampling_rate):
        '''
        An fast fourier transform (fft) method that uses resampling for fft calculations with resampling rate passed to the function
        
        Args:
            signal (array): The signal after filtering, e.g. RR intervals time series after filtering
            time_track (array): The time track  after filtering, effectively cum summed filtered RR intervals time series
            resampling_rate (float): The rate (in Hz) at which the signal (and the time - track) is to be resampled
        
        Returns:
            magnitude (float): magnitude of the fft
            phase (float): phase of the fft
            frequency_axis (float): frequency axis (from minimum to maximum (in the middle, and back)
        '''
        # now, since we want this to be a static method, we will call the resample function form the class
        signal_resampled, time_track_resampled = FFTSpectrum.resample(signal, time_track, resampling_rate)
        print(len(signal_resampled))
        X = np.fft.fft(signal_resampled)
        fundamental_frequency = 1 / time_track_resampled[-1]
        frequency_axis = np.cumsum(np.arange(len(time_track_resampled))) * fundamental_frequency
        magnitude = np.abs(X)
        phase = np.angle(X)
        return magnitude, phase, frequency_axis
