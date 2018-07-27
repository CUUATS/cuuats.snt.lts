import unittest
from blts_postgis import Blts
from cuuats.snt.lts.model.Segment import Segment
from cuuats.snt.lts.model.Approach import Approach

class BltsTest(unittest.TestCase):
    def test_environment_setup(self):
        segment = Segment()
        approaches = [Approach()]
        self.Blts = Blts(segment, approaches)
        self.assertEqual(self.Blts.bike_lane_without_adj_parking_score, 0)

    def test_calculate_score(self):
        segment = Segment()
        approaches = [Approach()]
        self.Blts = Blts(segment, approaches)
        # Test calculate score function
        aadt = [500, 1500, 3500]
        lanes_per_direction = [0, 1, 2, 3]
        score_matrix = [[1, 2, 3, 4],
                        [2, 3, 4, 4],
                        [3, 4, 4, 4]]
        outer_list = []
        inner_list = []
        for i in aadt:
            self.Blts.segment.aadt = i
            for l in lanes_per_direction:
                self.Blts.segment.lanes_per_direction = l
                score = self.Blts._calculate_score(
                    score_matrix,
                    ['self.segment.aadt <= 1000',
                     'self.segment.aadt <= 3000',
                     'True'],
                    ['self.segment.lanes_per_direction in (0, None)',
                     'self.segment.lanes_per_direction == 1',
                     'self.segment.lanes_per_direction == 2',
                     'self.segment.lanes_per_direction >= 3'])
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_mix_traffic(self):
        segment = Segment()
        approaches = [Approach()]
        self.Blts = Blts(segment, approaches)
        # Test the mix traffic function
        aadt = [500, 1500, 3500]
        lanes_per_direction = [0, 1, 2, 3]
        score_matrix = [[1, 2, 3, 4],
                        [2, 3, 4, 4],
                        [3, 4, 4, 4]]
        outer_list = []
        inner_list = []
        for i in aadt:
            self.Blts.segment.aadt = i
            for l in lanes_per_direction:
                self.Blts.segment.lanes_per_direction = l
                score = self.Blts._calculate_mix_traffic()
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_bikelane_with_adj_parking_one_lane(self):
        # Test Bike Facility and Parking Lane Width Filter
        segment = Segment()
        approaches = [Approach()]
        self.Blts = Blts(segment, approaches)
        # Test 1 Lane Per Direction or No lanes per direction
        lanes_per_direction = [None, 1]
        for l in lanes_per_direction:
            self.Blts.segment.lanes_per_direction = l
            aadt = [0, 1500, 3500, 50000]
            bicycle_facility_width = [10, 7, 4]
            parking_lane_width = [6, 7, 4]
            score_matrix = [[1, 2, 3],
                            [1, 2, 3],
                            [2, 3, 3],
                            [2, 4, 4]]
            outer_list = []
            inner_list = []
            for i in aadt:
                self.Blts.segment.aadt = i
                for (b, p) in zip(bicycle_facility_width, parking_lane_width):
                    self.Blts.segment.bicycle_facility_width = b
                    self.Blts.segment.parking_lane_width = p
                    score = self.Blts._calculate_bikelane_with_adj_parking()
                    inner_list.append(score)
                outer_list.append(inner_list)
                inner_list = []

            self.assertEqual(outer_list, score_matrix)

    def test_bikelane_with_adj_parking_one_lane(self):
        # Test Bike Facility and Parking Lane Width Filter
        segment = Segment()
        approaches = [Approach()]
        self.Blts = Blts(segment, approaches)
        # Test 1 Lane Per Direction or No lanes per direction
        lanes_per_direction = [None, 1]
        for l in lanes_per_direction:
            self.Blts.segment.lanes_per_direction = l
            aadt = [0, 1500, 3500, 50000]
            bicycle_facility_width = [10, 7, 4]
            parking_lane_width = [6, 7, 4]
            score_matrix = [[1, 2, 3],
                            [1, 2, 3],
                            [2, 3, 3],
                            [2, 4, 4]]
            outer_list = []
            inner_list = []
            for i in aadt:
                self.Blts.segment.aadt = i
                for (b, p) in zip(bicycle_facility_width, parking_lane_width):
                    self.Blts.segment.bicycle_facility_width = b
                    self.Blts.segment.parking_lane_width = p
                    score = self.Blts._calculate_bikelane_with_adj_parking()
                    inner_list.append(score)
                outer_list.append(inner_list)
                inner_list = []

            self.assertEqual(outer_list, score_matrix)

    def test_bikelane_with_adj_parking_two_lanes(self):
        segment = Segment()
        approaches = [Approach()]
        self.Blts = Blts(segment, approaches)
        self.Blts.segment.lanes_per_direction = 2
        aadt = [500, 3000, 30000, 30001]
        bicycle_facility_width = [10, 7]
        parking_lane_width = [5, 7]
        score_matrix = [[2, 3],
                        [2, 3],
                        [3, 3],
                        [3, 4]]
        outer_list = []
        inner_list = []
        for i in aadt:
            self.Blts.segment.aadt = i
            for (b, p) in zip(bicycle_facility_width, parking_lane_width):
                self.Blts.segment.bicycle_facility_width = b
                self.Blts.segment.parking_lane_width = p
                score = self.Blts._calculate_bikelane_with_adj_parking()
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_calculate_right_turn_lane(self):
        segment = Segment()
        approaches = [Approach()]
        self.Blts = Blts(segment, approaches)
        self.Blts.segment.functional_class = 4

        self.Blts.approach.lane_configuration = None
        self.Blts.approach.right_turn_lane_length = 0
        self.Blts.approach.bike_lane_approach = None
        # Test No Lane Configuration
        self.assertEqual(self.Blts._calculate_right_turn_lane(), 0)

        # Test condition 1
        self.Blts.approach.lane_configuration = "XXTR"
        self.Blts.approach.right_turn_lane_length = 120
        self.Blts.approach.bike_lane_approach = "Straight"
        self.assertEqual(self.Blts._calculate_right_turn_lane(), 2)

        # Test Condition 2
        self.Blts.approach.lane_configuration = "XXLTTR"
        self.Blts.approach.right_turn_lane_length = 151
        self.Blts.approach.bike_lane_approach = "Straight"
        self.assertEqual(self.Blts._calculate_right_turn_lane(), 3)

        # Test Condition 3
        self.Blts.approach.lane_configuration = "XXLTTR"
        self.Blts.approach.right_turn_lane_length = 151
        self.Blts.approach.bike_lane_approach = "Left"
        self.assertEqual(self.Blts._calculate_right_turn_lane(), 3)

        # Test Condition 4
        self.Blts.approach.lane_configuration = "XXLTTQ"
        self.Blts.approach.right_turn_lane_length = 151
        self.Blts.approach.bike_lane_approach = "Straight"
        self.assertEqual(self.Blts._calculate_right_turn_lane(), 4)

        self.Blts.approach.lane_configuration = "XXTR"
        self.Blts.approach.right_turn_lane_length = 120
        self.Blts.approach.bike_lane_approach = "Straight"
        self.assertEqual(self.Blts._calculate_right_turn_lane(), 2)

if __name__ == '__main__':
    unittest.main()
