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
        x = scipy.linspace(0.01, 2*scipy.pi, nin, dtype='float64')
        y = A * scipy.sin(B*x)
        self.signal4 = Signal([y, y*0, x]) # this is for the constructor that takes 3 elements

if __name__ == '__main__':
    unittest.main()