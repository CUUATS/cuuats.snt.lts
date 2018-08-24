# Unit Test for Segment Class
import unittest
from cuuats.snt.lts.model.Segment import Segment
from cuuats.snt.lts import config as c
import pandas as pd
from cuuats.snt.lts.lts_postgis import Lts


class SegmentTest(unittest.TestCase):
    def test_categorize_functional_class(self):
        segment = Segment()
        segment.functional_class = None
        self.assertEqual(segment._categorize_functional_class(), 'C')
        segment.functional_class = 4
        self.assertEqual(segment._categorize_functional_class(), 'C')
        segment.functional_class = 1
        self.assertEqual(segment._categorize_functional_class(), 'A')

    def test_calculate_mix_traffic(self):
        segment = Segment()
        segment.aadt = 1000
        segment.lanes_per_direction = 0
        self.assertEqual(segment._calculate_mix_traffic(), 1)

        segment.aadt = 1500
        segment.lanes_per_direction = 1
        self.assertEqual(segment._calculate_mix_traffic(), 3)

        segment.aadt = 3001
        segment.lanes_per_direction = 1
        self.assertEqual(segment._calculate_mix_traffic(), 4)


if __name__ == '__main__':
    unittest.main()
