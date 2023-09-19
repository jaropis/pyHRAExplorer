import unittest
from numpy import array
from signal_properties.RRclasses import Signal

class TestPoincareFiltering(unittest.TestCase):
    def setUp(self):
        self.signal1 = Signal([[980, 800, 850, 730, 710, 800, 801, 815, 900, 899, 750], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]])

    def test_pierwszy(self):
        self.assertTrue(self.signal1.signal[1] > 0)

if __name__ == '__main__':
    unittest.main()