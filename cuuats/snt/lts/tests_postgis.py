import unittest
from blts_postgis import Blts

class BltsTest(unittest.TestCase):
    def test_environment_setup(self):
        self.Blts = Blts()
        self.assertEqual(self.Blts.bike_lane_with_adj_parking_score, 0)

    def test_calculate_score(self):
        self.Blts = Blts()
        # Test calculate score function
        aadt = [500, 1500, 3500]
        lanes_per_direction = [0, 1, 2, 3]
        score_matrix = [[1, 2, 3, 4],
                        [2, 3, 4, 4],
                        [3, 4, 4, 4]]
        outer_list = []
        inner_list = []
        for i in aadt:
            self.Blts.aadt = i
            for l in lanes_per_direction:
                self.Blts.lanes_per_direction = l
                score = self.Blts._calculate_score(
                    score_matrix,
                    ['self.aadt <= 1000',
                     'self.aadt <= 3000',
                     'True'],
                    ['self.lanes_per_direction in (0, None)',
                     'self.lanes_per_direction == 1',
                     'self.lanes_per_direction == 2',
                     'self.lanes_per_direction >= 3'])
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_mix_traffic(self):
        self.Blts = Blts()
        # Test the mix traffic function
        aadt = [500, 1500, 3500]
        lanes_per_direction = [0, 1, 2, 3]
        score_matrix = [[1, 2, 3, 4],
                        [2, 3, 4, 4],
                        [3, 4, 4, 4]]
        outer_list = []
        inner_list = []
        for i in aadt:
            self.Blts.aadt = i
            for l in lanes_per_direction:
                self.Blts.lanes_per_direction = l
                score = self.Blts._calculate_mix_traffic()
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_bikelane_with_adj_parking_one_lane(self):
        # Test Bike Facility and Parking Lane Width Filter
        self.Blts = Blts()
        # Test 1 Lane Per Direction or No lanes per direction
        lanes_per_direction = [None, 1]
        for l in lanes_per_direction:
            self.Blts.lanes_per_direction = l
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
                self.Blts.aadt = i
                for (b, p) in zip(bicycle_facility_width, parking_lane_width):
                    self.Blts.bicycle_facility_width = b
                    self.Blts.parking_lane_width = p
                    score = self.Blts._calculate_bikelane_with_adj_parking()
                    inner_list.append(score)
                outer_list.append(inner_list)
                inner_list = []

            self.assertEqual(outer_list, score_matrix)

        def test_bikelane_with_adj_parking_one_lane(self):
            # Test Bike Facility and Parking Lane Width Filter
            self.Blts = Blts()
            # Test 1 Lane Per Direction or No lanes per direction
            lanes_per_direction = [None, 1]
            for l in lanes_per_direction:
                self.Blts.lanes_per_direction = l
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
                    self.Blts.aadt = i
                    for (b, p) in zip(bicycle_facility_width, parking_lane_width):
                        self.Blts.bicycle_facility_width = b
                        self.Blts.parking_lane_width = p
                        score = self.Blts._calculate_bikelane_with_adj_parking()
                        inner_list.append(score)
                    outer_list.append(inner_list)
                    inner_list = []

                self.assertEqual(outer_list, score_matrix)

    def test_bikelane_with_adj_parking_two_lanes(self):
        self.Blts = Blts()
        self.Blts.lanes_per_direction = 2
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
            self.Blts.aadt = i
            for (b, p) in zip(bicycle_facility_width, parking_lane_width):
                self.Blts.bicycle_facility_width = b
                self.Blts.parking_lane_width = p
                score = self.Blts._calculate_bikelane_with_adj_parking()
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

if __name__ == '__main__':
    unittest.main()
