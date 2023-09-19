import unittest
from signal_properties.RRclasses import Signal
from signal_properties.my_exceptions import WrongSignal

# I learned something - each test calls setup

class TestRuns(unittest.TestCase):
    def setUp(self):
        self.signal1 = Signal([[0, 2, 3, 4, 5], [0, 0, 0, 0, 0]]) # one decelerating run of length 4
        self.signal2 = Signal([[0, 2, 3, 4, 5, 4, 3, 2, 1], [0]*9]) # should be one dec run of lenght 4 and one acc of length 4
        self.signal3 = Signal([[4, 3, 2, 3, 2, 3, 2, 3, 2], [0]*9]) # 1 accelerating run of length 2 [3,2], then a
        # decelerating run [3], then an accelerating run [2], then a decelerating run [3], then an accelerating run [2]
        # then a decelerating run [3], then an accelerating run - so, 1 accelerating run of length 2, 3 accelerating
        # runs of length 1 and 3 decelerating runs of length 1
        self.signal4 = Signal([[1, 2, 3, 3, 3, 2, 1], [0, 0, 0, 0, 0, 0, 0]])
        self.signal5 = Signal([[1, 2, 3, 4, 3, 2, 1], [0, 0, 0, 1, 0, 0, 0]])
        self.signal6 = Signal([[10, 9, 8, 7, 6, 6, 6, 6, 5, 4, 3, 4, 5, 6], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
        self.signal1.set_runs()
        self.signal2.set_runs()
        self.signal3.set_runs()
        self.signal4.set_runs()
        self.signal5.set_runs()
        self.signal6.set_runs()
        # 1 acceleration of length 3, then 1 nutral run of length 2, then an acceleration run of length 3, then
        # a deceleration run of length 2 => dec_runs = [0, 1], acc_runs = [0, 0, 2], neutral_runs = [0, 1]


        #self.signal4 = Signal([[0,3,2,3,2,3,2,3,2], [0]*10]) # 4 accelerating runs of length 2

    # uncomment to test some internal methods - you will also need to uncomment them in the constructor
    # def test_segmentation(self): # uncomment to test the segmentation - also, in the constructor of the Runs class uncomment self.sinus_segments = self.split_on_annot(signal)
    #     # this method tests segmentation into segements of RRs of sinus origin (or "correct", if you are doing some other kind of analysis).
    #     #self.assertTrue((self.signal3.runs.sinus_segments == [array([3, 3.3, 3, 3.3, 3])]).all())
    #     self.assertTrue(allclose(self.signal3.runs.sinus_segments, [array([3, 3.3, 3, 3.3, 3])]))
    #     self.assertTrue(allclose(self.signal2.runs.sinus_segments, [array([3, 3.3]),  array([3.3, 3])]))
    #     self.assertTrue(allclose(self.signal3.runs.sinus_segments, [array([3.3, 3.2, 3.8]),  array([3.3, 0.5, 3.3])]))

    def test_count_runs_exception(self):
        signal = Signal([[3,2], [0,3]])
        self.assertRaises(WrongSignal, signal.set_runs) # this is how constructor of a class should be tested for exceptions!

    def test_runs_simple(self):
        # in the tests below we do not actually need .all(), because we are comparing regular lists - in the case of
        # scipy.array the comparisone is element-wise and we need .all()
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

        self.assertTrue(self.signal4.runs.dec_runs == [0, 1])
        self.assertTrue(self.signal4.runs.acc_runs == [0, 1])
        self.assertTrue(self.signal4.runs.neutral_runs == [0, 1])

    def test_runs_with_annotations(self):
        self.assertTrue(self.signal5.runs.dec_runs == [0, 1])
        self.assertTrue(self.signal5.runs.acc_runs == [0, 1])
        self.assertTrue(self.signal5.runs.neutral_runs == [])

        self.assertTrue(self.signal6.runs.dec_runs == [0, 1])
        self.assertTrue(self.signal6.runs.acc_runs == [0, 0, 2])
        self.assertTrue(self.signal6.runs.neutral_runs == [0, 1])

if __name__ == '__main__':
    unittest.main()
