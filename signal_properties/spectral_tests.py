import unittest
import scipy
from RRclasses import Signal
from numpy import allclose
from my_exceptions import WrongSignal

# I learned something - each test calls setup

class TestPoincareFiltering(unittest.TestCase):
    def setUp(self):
        pass
        # this needs to be cleaned up - these tests need to run only for certain classes, so the consturctor of Signal
        # needs to have a selector
        # self.signal1 = Signal([[1., 1., 1., 1.], [0, 0, 0, 0, 0]])
        # self.signal2 = Signal([[1., 1., 1., 1., 1.], [0, 0, 1., 0, 0]])
        # self.signal3 = Signal([[1., 2., 3., 4., 5., 6., 7., 8.], [1., 0, 0, 1., 0, 0, 0, 1.]])

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
        B = 1.
        nin = 1000
        x = scipy.linspace(0.01, 2*scipy.pi, nin)
        y = A * scipy.sin(B*(x + 0.5 * scipy.pi))
        self.signal4 = Signal([y, scipy.absolute(y*0), x]) # this is for the constructor that takes 3 elements
        # below is the integral over all the frequencies
        total_power = sum(self.signal4.LS_spectrum.periodogram) * (self.signal4.LS_spectrum.frequency[1] -  self.signal4.LS_spectrum.frequency[0])
        variance = scipy.var(self.signal4.signal)
        print(total_power, variance)
        self.assertAlmostEqual(total_power, variance, places=-1) # these should be VERY roughly equal
        # the variance of this signal should be \frac{1}{2\pi}\int_{-\pi}^{\pi} 8^2*sin^2(x) = 32
        # we can compare this result to both total power and total variance calculated from the data



if __name__ == '__main__':
    unittest.main()