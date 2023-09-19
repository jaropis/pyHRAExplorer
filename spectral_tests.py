import unittest
import scipy
from signal_properties.RRclasses import Signal
from signal_properties.my_exceptions import WrongCuts

# I learned something - each test calls setup

class TestLombSpectrum(unittest.TestCase):
    def setUp(self):
        pass
        # this needs to be cleaned up - these tests need to run only for certain classes, so the consturctor of Signal
        # needs to have a selector
        #self.signal1 = Signal([[1., 1., 1., 1.], [0, 0, 0, 0, 0]])
        #self.signal2 = Signal([[1., 1., 1., 1., 1.], [0, 0, 1., 0, 0]])
        #self.signal3 = Signal([[1., 2., 3., 4., 5., 6., 7., 8.], [1., 0, 0, 1., 0, 0, 0, 1.]])

    # def test_filter_and_timetrack(self):
    #     # testing filtering and time tracking
    #     self.assertTrue((self.signal1.LS_spectrum.filtered_signal == [1, 1, 1, 1]).all())
    #     self.assertTrue((self.signal1.LS_spectrum.filtered_time_track == [1, 2, 3, 4]).all())
    #
    #     self.assertTrue((self.signal2.LS_spectrum.filtered_signal == [1, 1, 1, 1]).all())
    #     self.assertTrue((self.signal2.LS_spectrum.filtered_time_track == [1, 2, 4, 5]).all())
    #
    #     self.assertTrue((self.signal3.LS_spectrum.filtered_signal == [2, 3, 5, 6, 7]).all())
    #     self.assertTrue((self.signal3.LS_spectrum.filtered_time_track == [3, 6, 15, 21, 28]).all())

    def test_full_signal_spectrum(self):
        A = 8.
        omega = 1.
        nin = 1000
        x = scipy.linspace(0.01, 2*scipy.pi, nin)
        y = A * scipy.sin(omega*(x + 0.5 * scipy.pi))
        self.signal4 = Signal([y, scipy.absolute(y*0), x]) # this is for the constructor that takes 3 elements
        self.signal4.set_LS_spectrum()
        # below is the integral over all the frequencies
        total_power = sum(self.signal4.LS_spectrum.periodogram) * (self.signal4.LS_spectrum.frequency[1] -  self.signal4.LS_spectrum.frequency[0])
        variance = scipy.var(self.signal4.signal)
        self.assertAlmostEqual(total_power, variance, places=-1)  # these should be VERY roughly equal
        # the variance of this signal should be \frac{1}{2\pi}\int_{-\pi}^{\pi} 8^2*sin^2(x) = 32
        # we can compare this result to both total power and total variance calculated from the data

    def test_get_bands(self):
        A1 = 8.
        omega1 = 1
        nin = 11
        x = scipy.linspace(0.01, 2*scipy.pi, nin)
        y1 = A1 * scipy.sin(omega1*(x))
        self.signal3 = Signal([y1, scipy.absolute(y1*0), x])
        self.signal3.set_LS_spectrum()
        # this signal will NOT be used - this is just to start somewhere
        self.signal3.LS_spectrum.periodogram = scipy.linspace(0.0, 1.0, nin) * 0 + 1.0/(nin-1) # this is just to test
        # if the segments add up to 0.5, as they should
        # so, the periodogram is [ 0.1  0.1  0.1  0.1  0.1  0.1  0.1  0.1  0.1  0.1  0.1]
        self.signal3.LS_spectrum.frequency = scipy.linspace(0.0, 1.0, nin)
        # and the frequencies are [ 0.   0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9  1. ]
        cuts = [0.0, 0.5, 1]
        self.assertTrue((self.signal3.LS_spectrum.get_bands(cuts, 1) == scipy.array([0.5, 0.5])).all())

    def test_test_cuts(self):
        cuts = [0.0, 0.5, 0.5, 1]
        A1 = 8.
        omega1 = 1
        nin = 11
        x = scipy.linspace(0.01, 2*scipy.pi, nin)
        y1 = A1 * scipy.sin(omega1*(x))
        self.signal3 = Signal([y1, scipy.absolute(y1*0), x])
        self.signal3.set_LS_spectrum()
        # this signal will NOT be used - this is just to start somewhere
        self.signal3.LS_spectrum.periodogram = scipy.linspace(0.0, 1.0, nin) * 0 + 1.0/(nin-1) # this is just to test
        # if the segments add up to 0.5, as they should
        # so, the periodogram is [ 0.1  0.1  0.1  0.1  0.1  0.1  0.1  0.1  0.1  0.1  0.1]
        self.signal3.LS_spectrum.frequency = scipy.linspace(0.0, 1.0, nin)
        # and the frequencies are [ 0.   0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9  1. ]
        self.assertRaises(WrongCuts, self.signal3.LS_spectrum.get_bands, [0.5, 0.5], df=1)

    def test_spectrum_bands(self):
        A1 = 8.
        A2 = 2.
        omega1 = 1
        omega2 = 2
        nin = 1000
        x = scipy.linspace(0.01, 2*scipy.pi, nin)
        y1 = A1 * scipy.sin(omega1*(x))
        y2 = A2 * scipy.sin(omega2*(x))
        y = y1+y2
        self.signal5 = Signal([y, scipy.absolute(y*0), x])
        self.signal5.set_LS_spectrum()
        self.signal51 = Signal([y1, scipy.absolute(y*0), x])
        self.signal51.set_LS_spectrum()
        self.signal52 = Signal([y2, scipy.absolute(y*0), x])
        self.signal52.set_LS_spectrum()
        variance = scipy.var(y)
        variance1 = scipy.var(y1)
        variance2 = scipy.var(y2)
        df = (self.signal5.LS_spectrum.frequency[1] -  self.signal5.LS_spectrum.frequency[0])
        print(df)
        spectral_content = self.signal5.LS_spectrum.get_bands(cuts=[0.2, 2.0], df=df)
        # this should be equal to the variance of the whole signal - the peaks are quite broad here, so wide integration interval
        spectral_content1 = self.signal51.LS_spectrum.get_bands(cuts=[0.2, 2.0], df=df)
        spectral_content2 = self.signal52.LS_spectrum.get_bands(cuts=[0.2, 2.5], df=df)
        self.assertAlmostEqual(spectral_content[0], variance, places = -1)
        self.assertAlmostEqual(spectral_content1[0], variance1, places = -1)
        self.assertAlmostEqual(spectral_content2[0], variance2, places = -1)

if __name__ == '__main__':
    unittest.main()
