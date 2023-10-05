from signal_properties.my_exceptions import WrongCuts
import numpy
import scipy.signal as sc
import numpy as np
import matplotlib.pyplot as plt


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
        bad_beats = numpy.where(signal.annotation != 0)[0]
        filtered_timetrack = numpy.delete(signal.timetrack, bad_beats)
        filtered_signal = numpy.delete(signal.signal, bad_beats)
        return filtered_signal, filtered_timetrack

    def build_spectrum(self):
        '''
        Method for creating a periodogram, showing the periodic behaviour in the time series

        Returns:
            frequency (array): Array with angular frequecies needed to build the periodogram
            periodogram (array): Array contaning the values of the periodogram, showing which angular frequencies are most common
        '''
        frequency = numpy.linspace(0.01, 2*numpy.pi, len(self.filtered_time_track))
        # here the assumption is that the frequencies are below 1Hz
        # which obviously may not be true
        periodogram = sc.lombscargle(self.filtered_time_track, self.filtered_signal, frequency) / len(self.filtered_time_track) * 4 * self.filtered_time_track[len(self.filtered_time_track)-1] / (2*numpy.pi) / 2
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
            first_index = numpy.where(self.frequency >= first)[0]
            second_index = numpy.where(self.frequency >= second)[0]
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
        return (numpy.array([i * df for i in power_in_bands]), power_in_bands)

    def test_cuts(self, cuts):
        '''
        Method for testing the validity of the cuts argument for the get_bands() method, raises WrongCuts if the cuts are unvalid

        Args:
            cuts (list): Holds the frequency bands of interest
        '''
        if len(cuts) != len(numpy.unique(cuts)) or (cuts != sorted(cuts)):
            raise WrongCuts
        
    def plot_periodogram(self, mode = 'angular', **kwargs):
        '''
        Method for plotting a periodogram
        '''
        frequency, x_label = (self.frequency/(2*np.pi), 'Frequency [Hz]') if mode == 'Hz' else (self.frequency, 'Angular frequency [rad/s]') 
        fig, periodogram_plot = plt.subplots()
        periodogram_plot.plot(frequency, self.periodogram, **kwargs)
        periodogram_plot.set_xlabel(x_label)
        periodogram_plot.set_ylabel('Amplitude')

        return periodogram_plot




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
        bad_beats = numpy.where(signal.annotation != 0)[0]
        filtered_timetrack = numpy.delete(signal.timetrack, bad_beats)
        filtered_signal = numpy.delete(signal.signal, bad_beats)
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
        from numpy.interpolate import interp1d
        f_interp = interp1d(time_track, signal)
        time_step = 1 / resampling_rate * 1000
        print(time_step)
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
