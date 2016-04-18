import unittest
from scipy import array
from RRclasses import Signal
from numpy import allclose
from my_exceptions import TooShortSignal

class TestPoincareFiltering(unittest.TestCase):
    def setUp(self):
        self.signal1 = Signal([[1, 1.1, 1, 1.1, 1], [0, 0, 0, 0, 0]])
        self.signal2 = Signal([[1, 1.1, 1, 1.1, 1], [0, 0, 1, 0, 0]])
        self.signal3 = Signal([[1, 1.1, 1.2, 1.8, 1, 1.3, 0.5, 1.1, 1], [2, 0, 0, 0, 1, 0, 0, 0, 2]])


    def test_segmentation(self):
        # this method tests segmentation into segements of RRs of sinus origin (or "correct", if you are doing some other kind of analysis).
        #self.assertTrue((self.signal1.runs.sinus_segments == [array([1, 1.1, 1, 1.1, 1])]).all())
        self.assertTrue(allclose(self.signal1.runs.sinus_segments, [array([1, 1.1, 1, 1.1, 1])]))
        self.assertTrue(allclose(self.signal2.runs.sinus_segments, [array([1, 1.1]),  array([1.1, 1])]))
        self.assertTrue(allclose(self.signal3.runs.sinus_segments, [array([1.1, 1.2, 1.8]),  array([1.3, 0.5, 1.1])]))

    def test_count_runs_exception(self):
        self.assertRaises(TooShortSignal, Signal, [[1,2], [0,1]])

if __name__ == '__main__':
    unittest.main()