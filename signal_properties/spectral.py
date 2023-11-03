from signal_properties.my_exceptions import WrongCuts
import numpy as np
import scipy.signal as sc
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd

class Spectrum:
    '''
    Class Spectrum for accessing, converting and plotting periodograms based on frequency and power

    Attributes:
        frequency_rad (array): Array with frequencies in rad/sec
        frequency_hz (array): Array with frequencies in Hz
        power (array): Power for a given frequency calculated during spectral analysis
        spectral_bands (dict):  A dictionary containing the names and total power within each band. 
        By default returns the vlf, lf, hf and tp values, correspondng to very low frequency, low frequency, high frequency and total power. When true, ulf or ultra law frequency can be calculated as well.

    '''
    def __init__(self, frequency, power, bands = [0.003, 0.04, 0.15, 0.4], mode = 'Hz', ulf = False):
        '''
        Initializes class Spectrum

        Args:
            frequency (array): An array with frequencies tested during spectral analysis
            power (array): Power at given frequencies calculated during spectral analysis
            mode (str): Specifies if the inputed frequency is in Hz or Rad/sec, Hz by default
            ulf (bool): Specifies if ultra low frequency should be calculated (for long term spectral analysis)
        '''
        
        self.frequency_rad, self.frequency_hz = self.frequency_conversion(frequency, mode) 
        self.power = power
        self.spectral_bands = self.get_bands((frequency, self.power))
        self.LF_HF_ratio = self.spectral_bands['lf']/self.spectral_bands['hf']

    def frequency_conversion(self, frequency, mode):
        '''
        Method for converting a given frequency into a frequency in Rad and Hz. 

        Args:
            frequency (array): An array with frequencies tested during spectral analysis
            mode (str): Specifies if the inputed frequency is in Hz or Rad/sec, Hz by default
        '''
        modes = ['Hz', 'Rad']
        if mode not in modes:
            raise ValueError("Invalid mode type. Select either 'Rad' or 'Hz'")
        rad_frequency, hz_frequency = (frequency*2*np.pi, frequency) if mode == 'Hz' else (frequency, frequency/(2*np.pi)) if mode == 'Rad' else (None, None)

        return rad_frequency, hz_frequency
    
    def get_bands(self, w_spectrum, bands=[0.003, 0.04, 0.15, 0.4], ulf=False):
        '''
        Method to calculate the spectral bands
        
        Args: 
            w_spectrum (tuple): A tuple containg the arrays corresponding to tested frequencies and the resulting power in spectrum
            bands (list): A list of bands for calculating the spectrum (in Hz)
            ulf (bool): Determines if ultra low frequency should be calculated. False by defualt
        
        Returns: 
            spectral_bands (dict): A dictionary with band names as keys and power in the corresponding bands as values
        '''
        #print("pierwsze bandy", bands, bands == [0.003, 0.04, 0.15, 0.4])
        if not ulf and bands == [0.003, 0.04, 0.15, 0.4]:
            bands = [0.04, 0.15, 0.4]
            band_names = ["vlf", "lf", "hf"]
        elif bands == [0.003, 0.04, 0.15, 0.4]:
            band_names = ["ulf", "vlf", "lf", "hf"]
        else:
            band_names = [str(_) for _ in bands]
        #print(bands, band_names)
        extended_bands = [0]; extended_bands.extend(bands)
        spectral_bands = []
        for band_idx in range(1, len(extended_bands)):
            spectral_bands.append(np.sum(np.abs(w_spectrum[1][np.logical_and(w_spectrum[0] > extended_bands[band_idx - 1],
                                                                  w_spectrum[0] <= extended_bands[band_idx])])))

        spectral_bands.append(np.sum(spectral_bands))
        band_names.append("tp")
        #results = pd.DataFrame([spectral_bands], columns=band_names)
        power_bands = dict(zip(band_names, spectral_bands))

        return power_bands

    def plot_spectrum(self, mode = 'Hz', xlim = [0, 0.4], color_bands = True, ulf = False, spectrum_units = '', **kwargs):
        '''
        Method for plotting a periodogram

        Args:
            mode (str): Specifies the mode of the plot, in Hz by default but can be changed into rad/sec, changing the mode changes
            the values and descriptions for the frequency (Hz = rad/sec / 2*pi)
            xlim (list): A list of values which is passed to determine the range of the x axis, full range shown by default
            color_bands (bool): Specifies if the spectral bands should be coloured
            ulf (bool): Determines if ultra low frequency should be displayed. False by defualt
            **kwargs: key word arguments which can be passed to the matplotlib.pyplots to change the appearance of the plot

        Returns:
            periodogram_plot (Axes): A plot showing the values of the periodogram against the frequency (either rad/sec or Hz)
        '''
        modes = ['Hz', 'Rad']
        if mode not in modes:
            raise ValueError("Invalid mode type. Select either 'Rad' or 'Hz'")
        frequency, x_label = (self.frequency_hz, 'Frequency [Hz]') if mode == 'Hz' else (self.frequency_rad, 'Angular frequency [rad/s]') 
        fig, periodogram_plot = plt.subplots()
        #periodogram_plot.plot(frequency, self.power, color = 'white', **kwargs, label = '_nolegend_')
        xlim = plt.xlim() if xlim == [] else xlim
        edge_cases = []
        if color_bands:
            if ulf:
                bands = [0, 0.003, 0.04, 0.15, 0.4]
                band_names = ['ulf', 'vlf', 'lf', 'hf']
            else:
                bands = [0, 0.04, 0.15, 0.4]
                band_names = ['vlf', 'lf', 'hf']
            colors = ['#E69F00', '#56B4E9', '#F0E442', '#009E73', '#0072B2']
            for i in range(1, len(bands)):
                #periodogram_plot.fill_between(x = frequency, y1 = self.power, where = (bands[i-1] < frequency)&(frequency < bands[i]), color = colors[i-1])
                periodogram_plot.fill_between(x = frequency, y1 = self.power, where = (bands[i-1] < frequency)&(frequency < bands[i]), color = colors[i-1], interpolate= True)
                #periodogram_plot.plot(x = frequency[bands[i-1], bands[i]], )
                #short_freq = frequency[np.logical_and(frequency > bands[i - 1], frequency <= bands[i])]
                #short_power = self.power[np.logical_and(frequency > bands[i - 1], frequency <= bands[i])]
                #periodogram_plot.plot(short_freq, short_power, color = colors[i-1], label = '_nolegend_')
                #edge_cases.append([short_freq[0], short_freq[-1]])
                #periodogram_plot.axvline(x = bands[i], ymin= 0, color = colors[i], label = '_nolegend_')
            #names = ['Spectrum']
            #names.extend(band_names)
            plt.legend(band_names, loc=0, frameon=True)
        periodogram_plot.set_xlim(xlim[0], xlim[1])
        periodogram_plot.set_xlabel(x_label)
        periodogram_plot.set_ylabel(('Power ' + spectrum_units))

        return periodogram_plot
        #return edge_cases



class LombScargleSpectrum:
    '''
    Class LombAcragleSpectrum used to build periodogram and perform spectral analysis
	
	Attributes:
		filtered_signal (array): An array with the filtered RR signal
	    filtered_timetrack (array): An array with the filtered timetrack
		frequency (array): Array with angular frequecies needed to build the periodogram
        periodogram (array): Array contaning the values of the periodogram, showing which angular frequencies are most common
        spectral_bands (dict): A dictionary containing the names and total power within each band. 
        By default returns the vlf, lf, hf and tp values, correspondng to very low frequency, low frequency, high frequency and total power.
        spectral_bands_24 (dict): A dictionary containing the names and total power within each band for long term spectral analysis. 
        By default the values of bands in Hz are used (vlf: 0-0.4, lf: 0.4-0.15, hf: 0.15-0.4)
        By default returns the ulf, vlf, lf, hf and tp values, correspondng to ultra low frequency, very low frequency, low frequency, high frequency and total power.
        By default the values of bands in Hz are used (ulf: 0-0.003, vlf: 0.003-0.4, lf: 0.4-0.15, hf: 0.15-0.4)
    '''
    def __init__(self, signal):
        '''
        Initiazes the LombScargleSpectrum

        Args:
	        signal (Signal): Object of class Signal containing signal, annotation and timetrack arrays
        '''
        self.filtered_signal, self.filtered_time_track = self.filter_and_timetrack(signal)
        self.periodogram, self.frequency = self.build_spectrum()
        self.spectral_bands = self.spectral_values()
        self.spectral_bands_24h = self.spectral_values(ulf = True)
        self.spectrum = Spectrum(self.frequency, self.periodogram)
        #self.ulf, self.vlf, self.lf, self.hf, self.tp = self.spectral_bands.values
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
            periodogram (array): Array contaning the values of the periodogram
        '''
        # old version 
        # CAREFUL! The old normalisation method no longer works!
        # frequency = np.linspace(0.01, 2*np.pi, len(self.filtered_time_track))
        # here the assumption is that the frequencies are below 1Hz which obviously may not be true
        # periodogram = sc.lombscargle(self.filtered_time_track, self.filtered_signal, frequency) / len(self.filtered_time_track) * 4 * self.filtered_time_track[len(self.filtered_time_track)-1] / (2*np.pi) / 2
        
        # new version 
        periodogram, frequency = self.lombscargle_press(self.filtered_signal)
        periodogram = periodogram * 1/len(periodogram) * np.var(self.filtered_signal)

        return periodogram, frequency
    
    def lombscargle_press(self, signal):
        '''
        Method calculating the Lombscargle spectrum using Press normalisation, adapted for python from the lomb function from lsc R package 
        
        Args:
            signal (Signal): Object of class Signal containing signal, annotation and timetrack arrays

        Returns:
            power (numpy.array): An array containing normalised values of amplitudes at each corresponding frequency
            frequency (numpy.array): An array containg the tested frequencies (in Hz)
        '''
        timetrack = np.cumsum(signal)/1000
        rr = signal

        ofac = 1 

        n = len(rr)
        timetrack_span = timetrack[n-1] - timetrack[0]
        fr_d = 1/timetrack_span
        step = 1/(timetrack_span * ofac)

        f_max = np.floor(0.5 * n * ofac) * step
        frequency = np.arange(fr_d, f_max, step)
        n_out = len(frequency)
        rr = rr - np.mean(rr)

        press_norm = 1/(2 * np.var(rr))

        w = 2 * np.pi * frequency
        power = [0] * n_out
        for i in range(0, n_out) :
            wi = w[i]
            tau = 0.5 * np.arctan2(sum(np.sin(wi * timetrack)), sum(np.cos(wi * timetrack)))/wi
            arg = wi * (timetrack - tau)
            cs = np.cos(arg)
            sn = np.sin(arg)
            A = (sum(rr * cs))**2
            B = sum(cs * cs)
            C = (sum(rr * sn))**2
            D = sum(sn * sn)
            power[i] = A/B + C/D

        power = np.array([i * press_norm for i in power])
        return power, frequency

    def get_spectral_bands(self, cuts):
        '''
        Method for calculating the spectral bands for a given set of cuts

        Args:
            cuts(list): Holds the frequency bands of interest
        
        Returns:
            power_in_bands (list): An array containing total power in each band (bands specified by cuts) 
        '''
        self.test_cuts(cuts)
        first = cuts[0]
        if first > max(self.frequency):
            return None
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
        return power_in_bands

    def get_bands(self, cuts, df):
        # OLD VERSION! Uisng an integration measure no longer works!
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
        return np.array([i * df for i in power_in_bands])

    def test_cuts(self, cuts):
        '''
        Method for testing the validity of the cuts argument for the get_bands() method, raises WrongCuts if the cuts are unvalid

        Args:
            cuts (list): Holds the frequency bands of interest
        '''
        if len(cuts) != len(np.unique(cuts)) or (cuts != sorted(cuts)):
            raise WrongCuts

    def spectral_values(self, cuts = [0.0, 0.04, 0.15, 0.4], ulf = False):
        """
        Method for calculating the spectral bands and assigning them to common spectral analysis parameters
        
        Args:
            ulf (logical): Specifies whether ulf should be calculated (should only be used for long reads)
        
        Return:
            results (dict): A dictionary with band names as keys and corresponding spectral bands as values
        """
        spectral_bands = []
        if ulf or cuts == [0.0, 0.003, 0.04, 0.15, 0.4]:
            band_names = ["ulf", "vlf", "lf", "hf"]
            spectral_bands = self.get_spectral_bands([0.0, 0.003, 0.04, 0.15, 0.4])
        elif not ulf or cuts == [0.0, 0.04, 0.15, 0.4]:
            band_names = ["vlf", "lf", "hf"]
            spectral_bands = self.get_spectral_bands([0.0, 0.04, 0.15, 0.4])
        else:
            band_names = [str(cut) for cut in cuts]
            spectral_bands = self.get_spectral_bands(cuts)
        if spectral_bands is None:
            return None
        spectral_bands.append(np.sum(spectral_bands))
        band_names.append("tp")
        #results = pd.DataFrame([spectral_bands], columns=band_names)
        results = dict(zip(band_names, spectral_bands))

        return results

        
    def plot_periodogram(self, mode = 'Hz', xlim = [], **kwargs):
        '''
        Method for plotting a periodogram

        Args:
            mode (str): Specifies the mode of the plot, in Hz by default but can be changed into rad/sec, changing the mode changes
            the values and descriptions for the frequency (Hz = rad/sec / 2*pi)
            xlim (list): A list of values which is passed to determine the range of the x axis, full range (0 - 6.28 for rad/sec or 0 - 1 for Hz) shown by default
            **kwargs: key word arguments which can be passed to the matplotlib.pyplots to change the appearance of the plot

        Returns:
            periodogram_plot (Axes): A plot showing the values of the periodogram against the frequency (either rad/sec or Hz)
        '''
        frequency, x_label = (self.frequency, 'Frequency [Hz]') if mode == 'Hz' else (self.frequency*(2*np.pi), 'Angular frequency [rad/s]') 
        fig, periodogram_plot = plt.subplots()
        periodogram_plot.plot(frequency, self.periodogram, **kwargs)
        xlim = plt.xlim() if xlim == [] else xlim
        periodogram_plot.set_xlim(xlim[0], xlim[1])
        periodogram_plot.set_xlabel(x_label)
        periodogram_plot.set_ylabel('Amplitude')

        return periodogram_plot



class WelchSpectrum:
    '''
    Class WelchSpectrum used to perform spectral analysis using the Welch method
	
	Attributes:
    timetrack (array): An array with timetrack values in ms
    interpolated_rr (array): An array containg interpolated signal values. 
    resampled_timetrack (array): An array containing resampled timetrack values.
    resampled_rr (array): An array contining resampled signal values
    welch_spectrum (tuple): A tuple containg the arrays corresponding to tested frequencies and the resulting power in the Welch spectrum
    welch_bands (dict): A dictionary storing the names and values of the spectral bands (vlf, lf, hf) and total power (tp) for short term spectral analysis
    welch_bands_24h (dict): A dictionary storing the names and values of the spectral bands (ulf, vlf, lf, hf) and total power (tp) for long term spectral analysis
    welch_bands_ulf (int): The value of the ultra low frequency band in the Welch spectrum (0.0-0.03 Hz) in the long term spectral analysis only
    welch_bands_vlf (int): The value of the very low frequency band in the Welch spectrum (0.0-0.4 Hz) in short term and (0.003-0.4 Hz) in long term spectral analysis
    welch_bands_lf (int): The value of the low frequency band in the Welch spectrum (0.04-0.15 Hz) 
    welch_bands_hf (int): The value of the high frequency band in the Welch spectrum (0.15-0.4 Hz)
    welch_bands_tp (int): The value of the total power in the Welch spectrum (0.0-0.4 Hz)
    '''

    def __init__(self, signal):
        '''
        Intializes the WelchSpectrum class

        Args:
            signal (Signal): Object of class Signal containing signal, annotation and timetrack arrays
        '''
        self.timetrack = np.cumsum(signal.signal)
        self.interpolated_rr = self.interpolate_non_sinus(signal)
        #self.test_resample = self.resample_rr(self.interpolated_rr, signal.timetrack)
        self.resampled_timetrack, self.resampled_rr = self.resample_rr(self.interpolated_rr, self.timetrack)
        self.welch_spectrum = self.calculate_welch(self.resampled_rr)
        self.onesided_welch_spectrum = self.onesided_ws(self.welch_spectrum)
        self.welch_bands = self.calculate_bands(self.welch_spectrum)
        self.welch_bands_24h = self.calculate_bands(self.welch_spectrum, ulf = True)
        self.welch_bands_ulf, self.welch_bands_vlf, self.welch_bands_lf, self.welch_bands_hf, self.welch_bands_tp = self.welch_bands_24h.values()
        self.spectrum = Spectrum(self.onesided_welch_spectrum[0], self.onesided_welch_spectrum[1])
    
    def interpolate_non_sinus(self, signal):
        """
        This method linearly interpolates the non-sinus beats
        
        Args:
            signal (Signal): Object of class Signal containing signal, annotation and timetrack arrays
        
        Returns:
            good_intervals (array): An array containg interpolated signal values. 
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
        good_intervals = np.concatenate(good_intervals_list)
        return good_intervals

    def optimal_division(self, signal, start, stop):
        '''
        Method for finding the optimal division

        Args:
            signal (Signal): Object of class Signal containing signal, annotation and timetrack arrays
            start (int): Index of the start of the segment
            stop (int): Index of the end of the segment
        
        Returns:
            optimal_division (array): Array with an optimal rr interval
        '''
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

    def resample_rr(self, signal, timetrack, period = 250, method = 'cubic'):
        """
        This method resamples the RR time series at period - the default value is 250 ms, which corresponds to 0.25 s or 4 Hz
        
        Args:
            signal (array): The RR intervals time series
            timetrack (array): Timetrack values
            period (int): Resampling period, default value 250 ms
            method (str):  Interpolation method, default is cubic splines

        Returns:
            timetrack_resampled (array): An array containing resampled timetrack values.
            rr_resampled (array): An array contining resampled signal values
        """
        #transforming timetrack from mins to sec
        '''timetrack = timetrack*60
        if period_type == 'Hz':
            period = 1 / period * 1000
        elif period_type == 'sec':
            period = period / 1000'''
        interp_object = interp1d(np.cumsum(signal), signal, kind=method, fill_value='extrapolate')
        # timetrack is in min, converting period in ms to min
        timetrack_resampled = np.arange(timetrack[0], timetrack[-1], step = period)
        rr_resampled = interp_object(timetrack_resampled)
        return timetrack_resampled, rr_resampled

    def calculate_welch(self, rr_resampled, fs=4, window='hamming', segment_min = 5,
                    noverlap_frac = 0.5):
        '''
        Method that calculates the Welch periodogram
        
        Args:
            rr_resampled (array): An array with resampled RR-intervals time series
            fs (int): Resampling frequency
            window (str): A type of window
            segment_min (int): Length of Welch segments in minutes
            noverlap_frac (float): Determines the value of the overlap, 0.5 by default
        
        Returns: 
            w_spectrum (tuple): A tuple containg the arrays corresponding to tested frequencies and the resulting power in the Welch spectrum
        '''
        w_spectrum = sc.welch(rr_resampled - np.mean(rr_resampled), fs=4, window=window, nperseg=segment_min * 60 * fs,
                       noverlap= segment_min * 60 * fs * noverlap_frac, return_onesided=False, scaling='spectrum')

        return w_spectrum

    def onesided_ws(self, w_spectrum):
        onesided_freq = w_spectrum[0][w_spectrum[0] >= 0]
        onesided_power = w_spectrum[1][w_spectrum[0] >= 0] * 2
        return onesided_freq, onesided_power
        

    def calculate_bands(self, w_spectrum, bands=[0.003, 0.04, 0.15, 0.4], ulf=False):
        '''
        Method to calculate the spectral bands
        
        Args: 
            w_spectrum (tuple): A tuple containg the arrays corresponding to tested frequencies and the resulting power in the Welch spectrum
            bands (list): A list of bands for calculating the Welch spectrum (in Hz)
            ulf (logical): Determines if ultra low frequency should be calculated. False by defualt
        
        Returns: 
            welch_bands (dict): A dictionary with band names as keys and power in the corresponding bands as values
        '''
        #print("pierwsze bandy", bands, bands == [0.003, 0.04, 0.15, 0.4])
        if not ulf and bands == [0.003, 0.04, 0.15, 0.4]:
            bands = [0.04, 0.15, 0.4]
            band_names = ["vlf", "lf", "hf"]
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
        welch_bands = dict(zip(band_names, spectral_bands))

        return welch_bands


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
