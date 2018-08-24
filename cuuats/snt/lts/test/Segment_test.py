# Unit Test for Segment Class
import unittest
from cuuats.snt.lts.model.Segment import Segment
from cuuats.snt.lts.model.BikePath import BikePath
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

    def test_calculate_bikelane_with_adj_parking(self):
        segment = Segment()
        segment.lanes_per_direction = 1
        segment.aadt = 900
        segment.parking_lane_width = 5
        bike_path = BikePath(width=16)
        self.assertEqual(
            segment._calculate_bikelane_with_adj_parking(bike_path), 1)

        segment.lanes_per_direction = 2
        segment.aadt = 900
        segment.parking_lane_width = 5
        bike_path = BikePath(width=16)
        self.assertEqual(
            segment._calculate_bikelane_with_adj_parking(bike_path), 2)

        segment.lanes_per_direction = 2
        segment.aadt = 3000
        segment.parking_lane_width = 5
        bike_path = BikePath(width=6)
        self.assertEqual(
            segment._calculate_bikelane_with_adj_parking(bike_path), 3)

        segment.lanes_per_direction = 1
        segment.aadt = 35000
        segment.parking_lane_width = 6
        bike_path = BikePath(width=8)
        self.assertEqual(
            segment._calculate_bikelane_with_adj_parking(bike_path), 4)

    def test_calculate_bikelane_without_adj_parking(self):
        segment = Segment()
        segment.lanes_per_direction = 1
        segment.aadt = 900
        segment.parking_lane_width = None
        bike_path = BikePath(width=8)
        self.assertEqual(
            segment._calculate_bikelane_without_adj_parking(bike_path), 1)

        segment.lanes_per_direction = None
        segment.aadt = 4000
        segment.parking_lane_width = None
        bike_path = BikePath(width=6)
        self.assertEqual(
            segment._calculate_bikelane_without_adj_parking(bike_path), 3)

        segment.lanes_per_direction = 2
        segment.aadt = 35000
        segment.parking_lane_width = None
        bike_path = BikePath(width=8)
        self.assertEqual(
            segment._calculate_bikelane_without_adj_parking(bike_path), 3)

        segment.lanes_per_direction = 3
        segment.aadt = 7000
        segment.parking_lane_width = None
        bike_path = BikePath(width=7)
        self.assertEqual(
            segment._calculate_bikelane_without_adj_parking(bike_path), 2)


if __name__ == '__main__':
    unittest.main()
