import unittest
from Poincare import Poincare
from signal_properties.RRclasses import *


class TestPoincareFiltering(unittest.TestCase):

    def setUp(self):
        self.signal_real = Signal("RR.csv", 2, 3, annotation_filter = (2,))