import unittest
from signal_properties.RRclasses import Signal
from numpy import array


class TestPoincareFiltering(unittest.TestCase):

    def setUp(self):
        self.signal1 = Signal([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],
                            annotation_filter = (1,)) # testing annotation filter inside
        self.signal1.set_poincare()
        self.signal2 = Signal([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 0, 0, 0, 0, 0, 0 , 0 ,0]],
                            annotation_filter = (1,)) # testing annotation filter in the beginning
        self.signal2.set_poincare()
        self.signal3 = Signal([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 0, 0, 0, 0, 0, 0, 0 , 1 ,1]],
                            annotation_filter = (1,)) # testing annotation filter in the beginning
        self.signal3.set_poincare()
        self.signal4 = Signal([[751, 802, 753, 804, 755, 8006, 757, 808, 759, 810], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                              square_filter = (0, 2000)) # testing square filter in the middle
        self.signal4.set_poincare()
        self.signal5 = Signal([[7051, 200, 753, 804, 755, 806, 757, 808, 759, 810], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                              square_filter = (300, 2000)) # testing square filter in the middle
        self.signal5.set_poincare()
        self.signal6 = Signal([[751, 802, 753, 804, 755, 806, 757, 808, 7059, 8010], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],
                  square_filter = (300, 2000), annotation_filter = (1,)) # testing square filter in the middle
        self.signal6.set_poincare()
        # testing quality parameters
        self.signal7 = Signal([[751, 802, 753, 804, 755, 806, 757, 808, 7059, 8010], [0, 0, 0, 1, 0, 2, 0, 1, 0, 0]], annotation_filter = (1,))
        self.signal8 = Signal([[751, 802, 753, 804, 755, 806, 757, 808, 7059, 8010], [4, 0, 0, 1, 2, 2, 0, 1, 0, 3]], annotation_filter = (1,))
        self.signal9 = Signal([[751, 802, 753, 804, 755, 806, 757, 808, 7059, 8010], [4, 0, 0, 0, 2, 2, 3, 1, 6, 6]], annotation_filter = (1,))


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

    def test_quality(self):
        # Signal7: 10 beats total, 7 with '0' flag, 2 with '1' flag, 1 with '2' flag, 0 with '3' flag and 0 with unknown flag 
        self.assertTrue((self.signal7.quality_counts == [10, 7, 2, 1, 0, 0]))
        self.assertTrue((self.signal7.n_s == 7)) # number of sinus beats ('0' flag)
                # Signal7: 10 beats total, 4 with '0' flag, 2 with '1' flag, 2 with '2' flag, 1 with '3' flag and 1 with unknown flag 
        self.assertTrue((self.signal8.quality_counts == [10, 4, 2, 2, 1, 1]))
        self.assertTrue((self.signal8.n_x == 1)) # number of artifacts (flag '3')
                # Signal7: 10 beats total, 3 with '0' flag, 1 with '1' flag, 2 with '2' flag, 1 with '3' flag and 3 with unknown flag 
        self.assertTrue((self.signal9.quality_counts == [10, 3, 1, 2, 1, 3]))
        # is the sum of all flags equal to the toatla number of beats?
        self.assertTrue((self.signal9.n_s + self.signal9.n_v + self.signal9.n_sv + self.signal9.n_x + self.signal9.n_u) == self.signal9.n_total)

        

if __name__ == '__main__':
    unittest.main()