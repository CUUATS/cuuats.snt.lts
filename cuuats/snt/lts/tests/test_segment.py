# Unit Test for Segment Class
import unittest
from cuuats.snt.lts import Segment, BikePath, Approach, Sidewalk, Crossing


class TestSegment(unittest.TestCase):
    def test_categorize_functional_class(self):
        segment = Segment()
        self.assertEqual(segment._categorize_functional_class(None), 'C')
        self.assertEqual(segment._categorize_functional_class(4), 'C')
        self.assertEqual(segment._categorize_functional_class(1), 'A')

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

        segment.lanes_per_direction = 1
        segment.aadt = 35000
        segment.parking_lane_width = None
        bike_path = BikePath(width=8)
        self.assertEqual(
            segment._calculate_bikelane_with_adj_parking(bike_path),
            float('Inf'))

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

        segment.lanes_per_direction = 3
        segment.aadt = 7000
        segment.parking_lane_width = 5
        bike_path = BikePath(width=7)
        self.assertEqual(
            segment._calculate_bikelane_without_adj_parking(bike_path), 99)

    def test_right_turn_lane(self):
        segment = Segment(functional_class=4)
        approach = Approach(lane_configuration="XXTR",
                            right_turn_lane_length=50,
                            bike_lane_approach='Straight')
        self.assertEqual(
            segment._calculate_right_turn_lane(approach), 0)

        segment = Segment(functional_class=3)
        approach = Approach(lane_configuration="XXTR",
                            right_turn_lane_length=150,
                            bike_lane_approach='Straight')
        self.assertEqual(
            segment._calculate_right_turn_lane(approach), 2)

        segment = Segment(functional_class=1)
        approach = Approach(lane_configuration="XXTTR",
                            right_turn_lane_length=151,
                            bike_lane_approach='Straight')
        self.assertEqual(
            segment._calculate_right_turn_lane(approach), 3)

        segment = Segment(functional_class=1)
        approach = Approach(lane_configuration="XXTTR",
                            right_turn_lane_length=151,
                            bike_lane_approach='Left')
        self.assertEqual(
            segment._calculate_right_turn_lane(approach), 3)

        segment = Segment(functional_class=1)
        approach = Approach(lane_configuration="XXTTQ",
                            right_turn_lane_length=151,
                            bike_lane_approach=None)
        self.assertEqual(
            segment._calculate_right_turn_lane(approach), 4)

    def test_left_turn_lane(self):
        segment = Segment(functional_class=4,
                          posted_speed=25)
        approach = Approach(lane_configuration="XXLT")
        self.assertEqual(
            segment._calculate_left_turn_lane(approach), 0)

        segment = Segment(functional_class=3,
                          posted_speed=25)
        approach = Approach(lane_configuration="XXT")
        self.assertEqual(
            segment._calculate_left_turn_lane(approach), 2)

        segment = Segment(functional_class=3,
                          posted_speed=30)
        approach = Approach(lane_configuration="XXTT")
        self.assertEqual(
            segment._calculate_left_turn_lane(approach), 3)

        segment = Segment(functional_class=3,
                          posted_speed=30)
        approach = Approach(lane_configuration="XXTTR")
        self.assertEqual(
            segment._calculate_left_turn_lane(approach), 4)

        segment = Segment(functional_class=3,
                          posted_speed=35)
        approach = Approach(lane_configuration="XXTTR")
        self.assertEqual(
            segment._calculate_left_turn_lane(approach), 4)

        segment = Segment(functional_class=3,
                          posted_speed=25)
        approach = Approach(lane_configuration="XXLT")
        self.assertEqual(
            segment._calculate_left_turn_lane(approach), 4)

    def test_sidewalk_cond(self):
        segment = Segment()
        sidewalk = Sidewalk(sidewalk_width=7,
                            sidewalk_score=80)
        self.assertEqual(segment._calculate_condition_score(sidewalk), 1)

        sidewalk = Sidewalk(sidewalk_width=6,
                            sidewalk_score=65)
        self.assertEqual(segment._calculate_condition_score(sidewalk), 2)

        sidewalk = Sidewalk(sidewalk_width=5,
                            sidewalk_score=55)
        self.assertEqual(segment._calculate_condition_score(sidewalk), 3)

        sidewalk = Sidewalk(sidewalk_width=4,
                            sidewalk_score=69)
        self.assertEqual(segment._calculate_condition_score(sidewalk), 3)

        sidewalk = Sidewalk(sidewalk_width=None,
                            sidewalk_score=None)
        self.assertEqual(segment._calculate_condition_score(sidewalk), 4)

    def test_sidewalk_buffer_type(self):
        segment = Segment(posted_speed=25)
        sidewalk = Sidewalk(buffer_type=None)
        self.assertEqual(segment._calculate_buffer_type_score(sidewalk), 2)

        segment = Segment(posted_speed=30)
        sidewalk = Sidewalk(buffer_type="landscaped")
        self.assertEqual(segment._calculate_buffer_type_score(sidewalk), 2)

        segment = Segment(posted_speed=45)
        sidewalk = Sidewalk(buffer_type="no buffer")
        self.assertEqual(segment._calculate_buffer_type_score(sidewalk), 4)

        segment = Segment(posted_speed=35)
        sidewalk = Sidewalk(buffer_type="landscaped")
        self.assertEqual(segment._calculate_buffer_type_score(sidewalk), 2)

        segment = Segment(posted_speed=40)
        sidewalk = Sidewalk(buffer_type="landscaped with trees")
        self.assertEqual(segment._calculate_buffer_type_score(sidewalk), 2)

        segment = Segment(posted_speed=25)
        sidewalk = Sidewalk(buffer_type="solid buffer")
        self.assertEqual(segment._calculate_buffer_type_score(sidewalk), 1)

        segment = Segment(posted_speed=None)
        sidewalk = Sidewalk(buffer_type=None)
        self.assertEqual(segment._calculate_buffer_type_score(sidewalk), 2)

        segment = Segment(posted_speed=30)
        sidewalk = Sidewalk(buffer_type='solid surface')
        self.assertEqual(segment._calculate_buffer_type_score(sidewalk), 2)

        segment = Segment(posted_speed=35)
        sidewalk = Sidewalk(buffer_type='')
        self.assertEqual(segment._calculate_buffer_type_score(sidewalk), 3)

    def test_buffer_width(self):
        segment = Segment(total_lanes=2)
        sidewalk = Sidewalk(buffer_width=5)
        self.assertEqual(segment._calculate_buffer_width_score(sidewalk), 2)

        segment = Segment(total_lanes=3)
        sidewalk = Sidewalk(buffer_width=15)
        self.assertEqual(segment._calculate_buffer_width_score(sidewalk), 1)

        segment = Segment(total_lanes=5)
        sidewalk = Sidewalk(buffer_width=4.9)
        self.assertEqual(segment._calculate_buffer_width_score(sidewalk), 4)

        segment = Segment(total_lanes=4)
        sidewalk = Sidewalk(buffer_width=7)
        self.assertEqual(segment._calculate_buffer_width_score(sidewalk), 3)

        segment = Segment(total_lanes=6)
        sidewalk = Sidewalk(buffer_width=20)
        self.assertEqual(segment._calculate_buffer_width_score(sidewalk), 2)

        segment = Segment(total_lanes=0)
        sidewalk = Sidewalk(buffer_width=20)
        self.assertEqual(segment._calculate_buffer_width_score(sidewalk), 1)

        segment = Segment(total_lanes=0)
        sidewalk = Sidewalk(buffer_width=None)
        self.assertEqual(segment._calculate_buffer_width_score(sidewalk), 2)

    def test_off_street_trail(self):
        segment = Segment()
        bike_path = BikePath(path_category='Off-Street Trail')
        self.assertTrue(segment._find_off_street_trail(bike_path))

        bike_path = BikePath(path_category='Other Trail')
        self.assertFalse(segment._find_off_street_trail(bike_path))

    def test_no_median_crossing(self):
        segment = Segment()
        crossing = Crossing(crossing_speed=25, lanes=3)
        self.assertEqual(segment._calculate_crossing_without_median(crossing),
                         1)

        crossing = Crossing(crossing_speed=30, lanes=4)
        self.assertEqual(segment._calculate_crossing_without_median(crossing),
                         2)

        crossing = Crossing(crossing_speed=35, lanes=5)
        self.assertEqual(segment._calculate_crossing_without_median(crossing),
                         3)

        crossing = Crossing(crossing_speed=40, lanes=6)
        self.assertEqual(segment._calculate_crossing_without_median(crossing),
                         4)

    def test_has_median_crossing(self):
        segment = Segment()
        crossing = Crossing(crossing_speed=25, lanes=1)
        self.assertEqual(segment._calculate_crossing_with_median(crossing), 1)

        crossing = Crossing(crossing_speed=30, lanes=2)
        self.assertEqual(segment._calculate_crossing_with_median(crossing), 1)

        crossing = Crossing(crossing_speed=35, lanes=3)
        self.assertEqual(segment._calculate_crossing_with_median(crossing), 3)

        crossing = Crossing(crossing_speed=35, lanes=2)
        self.assertEqual(segment._calculate_crossing_with_median(crossing), 2)

        crossing = Crossing(crossing_speed=40, lanes=4)
        self.assertEqual(segment._calculate_crossing_with_median(crossing), 4)

    def test_collector_crossing(self):
        segment = Segment()
        crossing = Crossing(crossing_speed=25, lanes=1, functional_class=4)
        self.assertEqual(segment._calcualate_collector_crossing_wo_med(
                crossing), 1)

        crossing = Crossing(crossing_speed=35, lanes=1, functional_class=4)
        self.assertEqual(segment._calcualate_collector_crossing_wo_med(
                crossing), 2)

        crossing = Crossing(crossing_speed=30, lanes=2, functional_class=4)
        self.assertEqual(segment._calcualate_collector_crossing_wo_med(
                crossing), 2)

        crossing = Crossing(crossing_speed=40, lanes=2, functional_class=4)
        self.assertEqual(segment._calcualate_collector_crossing_wo_med(
                crossing), 3)

    def test_arterial_crossing_two_lanes(self):
        segment = Segment()
        crossing = Crossing(crossing_speed=25, lanes=2, aadt=4000)
        self.assertEqual(segment._calculate_art_crossing_wo_med_two_lanes(
                crossing), 2)

        crossing = Crossing(crossing_speed=30, lanes=2, aadt=6000)
        self.assertEqual(segment._calculate_art_crossing_wo_med_two_lanes(
                crossing), 3)

        crossing = Crossing(crossing_speed=35, lanes=2, aadt=8000)
        self.assertEqual(segment._calculate_art_crossing_wo_med_two_lanes(
                crossing), 3)

        crossing = Crossing(crossing_speed=40, lanes=2, aadt=10000)
        self.assertEqual(segment._calculate_art_crossing_wo_med_two_lanes(
                crossing), 4)

    def test_arterial_crossing_three_lanes(self):
        segment = Segment()
        crossing = Crossing(crossing_speed=25, lanes=3, aadt=4000)
        self.assertEqual(segment._calculate_art_crossing_wo_med_three_lanes(
                crossing), 3)

        crossing = Crossing(crossing_speed=30, lanes=3, aadt=6000)
        self.assertEqual(segment._calculate_art_crossing_wo_med_three_lanes(
                crossing), 3)

        crossing = Crossing(crossing_speed=35, lanes=3, aadt=10000)
        self.assertEqual(segment._calculate_art_crossing_wo_med_three_lanes(
                crossing), 4)

        crossing = Crossing(crossing_speed=40, lanes=3, aadt=12000)
        self.assertEqual(segment._calculate_art_crossing_wo_med_three_lanes(
                crossing), 4)


if __name__ == '__main__':
    unittest.main()
