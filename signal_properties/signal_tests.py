import unittest
from numpy import array

from signal_properties.RRclasses import *

class TestPoincareFiltering(unittest.TestCase):

    def setUp(self):
        self.signal1 = Signal([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],
                            annotation_filter=(1,)) # testing annotation filter inside
        self.signal2 = Signal([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 0, 0, 0, 0, 0, 0 , 0 ,0]],
                            annotation_filter=(1,)) # testing annotation filter in the beginning
        self.signal3 = Signal([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 0, 0, 0, 0, 0, 0, 0 , 1 ,1]],
                            annotation_filter=(1,)) # testing annotation filter in the beginning

    def test_the_middle(self):
        self.assertTrue((self.signal1.poincare.xi == array([1, 2, 5, 6, 7, 8, 9])).all()) ## test for xi
        self.assertTrue((self.signal1.poincare.xii == array([2, 3, 6, 7, 8, 9, 10])).all()) ## test for xii

    def test_the_beginning(self):
        self.assertTrue((self.signal2.poincare.xi == array([3, 4, 5, 6, 7, 8, 9])).all()) # test for xi
        self.assertTrue((self.signal2.poincare.xii == array([4, 5, 6, 7, 8, 9, 10])).all()) # test for xii

    def test_the_end(self):
        self.assertTrue((self.signal3.poincare.xi == array([1, 2, 3, 4, 5, 6, 7])).all()) ## test for xi
        self.assertTrue((self.signal3.poincare.xii == array([2,3,4, 5, 6, 7, 8])).all()) ## test for xii

if __name__ == '__main__':
    unittest.main()