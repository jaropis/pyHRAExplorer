import unittest
from scipy import array
from RRclasses import Signal
from numpy import allclose
from my_exceptions import WrongSignal

# I learned something - each test calls setup

class TestPoincareFiltering(unittest.TestCase):
    def setUp(self):
        self.signal1 = Signal([[0, 2, 3, 4, 5], [0, 0, 0, 0, 0]]) # one decelerating run of length 4
        self.signal2 = Signal([[0, 2, 3, 4, 5, 4, 3, 2, 1], [0]*9]) # should be one dec run of lenght 4 and one acc of length 4
        self.signal3 = Signal([[4, 3, 2, 3, 2, 3, 2, 3, 2], [0]*9]) # 1 accelerating run of length 2 [3,2], then a
        # decelerating run [3], then an accelerating run [2], then a decelerating run [3], then an accelerating run [2]
        # then a decelerating run [3], then an accelerating run - so, 1 accelerating run of length 2, 3 accelerating
        # runs of length 1 and 3 decelerating runs of length 1

        #self.signal4 = Signal([[0,3,2,3,2,3,2,3,2], [0]*10]) # 4 accelerating runs of length 2

    # def test_segmentation(self): # uncomment to test the segmentation - also, in the constructor of the Runs class uncomment self.sinus_segments = self.split_on_annot(signal)
    #     # this method tests segmentation into segements of RRs of sinus origin (or "correct", if you are doing some other kind of analysis).
    #     #self.assertTrue((self.signal3.runs.sinus_segments == [array([3, 3.3, 3, 3.3, 3])]).all())
    #     self.assertTrue(allclose(self.signal3.runs.sinus_segments, [array([3, 3.3, 3, 3.3, 3])]))
    #     self.assertTrue(allclose(self.signal2.runs.sinus_segments, [array([3, 3.3]),  array([3.3, 3])]))
    #     self.assertTrue(allclose(self.signal3.runs.sinus_segments, [array([3.3, 3.2, 3.8]),  array([3.3, 0.5, 3.3])]))

    def test_count_runs_exception(self):
        self.assertRaises(WrongSignal, Signal, [[3,2], [0,3]]) # this is how constructor of a class should be tested for exceptions!

    def test_runs_simple(self):
        #print(self.signal1.runs.dec_runs)
        self.assertTrue(self.signal1.runs.dec_runs == [0, 0, 0, 1])
        self.assertTrue(self.signal1.runs.acc_runs == [])
        self.assertTrue(self.signal1.runs.neutral_runs == [])

        self.assertTrue(self.signal2.runs.dec_runs == [0, 0, 0, 1])
        self.assertTrue(self.signal2.runs.acc_runs == [0, 0, 0, 1])
        self.assertTrue(self.signal2.runs.neutral_runs == [])

        # this one is tricky - see above in the comments
        self.assertTrue(self.signal3.runs.dec_runs == [3])
        self.assertTrue(self.signal3.runs.acc_runs == [3, 1])
        self.assertTrue(self.signal3.runs.neutral_runs == [])

if __name__ == '__main__':
    unittest.main()