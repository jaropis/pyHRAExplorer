import unittest
from numpy import array

from signal_properties.RRclasses import *

class TestPoincareFiltering(unittest.TestCase):

    def setUp(self):
        self.signal1 = Signal([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],
                            annotation_filter = (1,)) # testing annotation filter inside
        self.signal2 = Signal([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 0, 0, 0, 0, 0, 0 , 0 ,0]],
                            annotation_filter = (1,)) # testing annotation filter in the beginning
        self.signal3 = Signal([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 0, 0, 0, 0, 0, 0, 0 , 1 ,1]],
                            annotation_filter = (1,)) # testing annotation filter in the beginning
        self.signal4 = Signal([[751, 802, 753, 804, 755, 8006, 757, 808, 759, 810], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                              square_filter = (0, 2000)) # testing square filter in the middle
        self.signal5 = Signal([[7051, 200, 753, 804, 755, 806, 757, 808, 759, 810], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                              square_filter = (300, 2000)) # testing square filter in the middle
        self.signal6 = Signal([[751, 802, 753, 804, 755, 806, 757, 808, 7059, 8010], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],
                  square_filter = (300, 2000), annotation_filter = (1,)) # testing square filter in the middle
        self.signal_real = Signal("../0001.rea", 2, 3, annotation_filter = (2,))


    def test_the_middle(self):
        self.assertTrue((self.signal1.poincare.xi == array([1, 2, 5, 6, 7, 8, 9])).all()) ## test for xi
        self.assertTrue((self.signal1.poincare.xii == array([2, 3, 6, 7, 8, 9, 10])).all()) ## test for xii

    def test_the_beginning(self):
        self.assertTrue((self.signal2.poincare.xi == array([3, 4, 5, 6, 7, 8, 9])).all()) # test for xi
        self.assertTrue((self.signal2.poincare.xii == array([4, 5, 6, 7, 8, 9, 10])).all()) # test for xii

    def test_the_end(self):
        self.assertTrue((self.signal3.poincare.xi == array([1, 2, 3, 4, 5, 6, 7])).all()) ## test for xi
        self.assertTrue((self.signal3.poincare.xii == array([2, 3, 4, 5, 6, 7, 8])).all()) ## test for xii

    def test_square_middle(self):
        self.assertTrue((self.signal4.poincare.xi == array([751, 802, 753, 804, 757, 808, 759])).all())
        self.assertTrue((self.signal4.poincare.xii == array([802, 753, 804, 755, 808, 759, 810])).all())

    def test_square_beginning(self):
        self.assertTrue((self.signal5.poincare.xi == array([753, 804, 755, 806, 757, 808, 759])).all())
        self.assertTrue((self.signal5.poincare.xii == array([804, 755, 806, 757, 808, 759, 810])).all())

    def test_square_end_mixed(self):
        self.assertTrue((self.signal6.poincare.xi == array([751, 802, 755, 806, 757])).all())
        self.assertTrue((self.signal6.poincare.xii == array([802, 753, 806, 757, 808])).all())

    def test_classic_descriptors(self): # the results are calculated according to the hrstruct.org tutorial, using the datafile from this same source
        pass
if __name__ == '__main__':
    unittest.main()