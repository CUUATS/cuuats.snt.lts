import unittest
from blts_cuuats import calculate_score, calculate_mix_traffic, \
    calculate_bikelane_with_adj_parking, \
    calculate_bikelane_without_adj_parking, calculate_max_lane, \
    calculate_lanecrossed, aggregate_score, calculate_right_turn_lane, \
    calculate_left_turn_lane, calculate_unsignalized_crossing_without_median, \
    calculate_unsignalized_crossing_with_median
from plts_cuuats import calculate_sidewalk_conditions, \
    calculate_physical_buffer, calculate_general_landuse, \
    calculate_total_buffering_width, convert_score, convert_feet_to_inches, \
    calculate_total_lanes_crossed, categorize_functional_class, \
    calculate_unsignalized_collector_crossing_score, \
    calculate_unsignalized_arterial_crossing_score

class TestBLTS(unittest.TestCase):
    PostedSpeed = 50
    BikeLaneWidth = 10
    IDOTAADT = 500
    LanesPerDirection = None

    def test_environment_setup(self):
        self.assertEqual(self.IDOTAADT, 500)
        self.assertTrue(self.LanesPerDirection is None)
        self.TestData = 500
        self.assertEqual(self.TestData, 500)

    def test_calculate_score(self):
        # Test calculate score function
        IDOTAADT = [500, 1500, 3500]
        LanesPerDirection = [0, 1, 2, 3]
        score_matrix = [[1, 2, 3, 4],
                        [2, 3, 4, 4],
                        [3, 4, 4, 4]]
        outer_list = []
        inner_list = []
        for i in IDOTAADT:
            self.IDOTAADT = i
            for l in LanesPerDirection:
                self.LanesPerDirection = l
                score = calculate_score(
                    self,
                    score_matrix,
                    ['self.IDOTAADT <= 1000',
                     'self.IDOTAADT <= 3000',
                     'True'],
                    ['self.LanesPerDirection in (0, None)',
                     'self.LanesPerDirection == 1',
                     'self.LanesPerDirection == 2',
                     'self.LanesPerDirection >= 3'])
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_mix_traffic(self):
        # Test the mix traffic function
        IDOTAADT = [500, 1500, 3500]
        LanesPerDirection = [0, 1, 2, 3]
        score_matrix = [[1, 2, 3, 4],
                        [2, 3, 4, 4],
                        [3, 4, 4, 4]]
        outer_list = []
        inner_list = []
        for i in IDOTAADT:
            self.IDOTAADT = i
            for l in LanesPerDirection:
                self.LanesPerDirection = l
                score = calculate_mix_traffic(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_bikelane_with_adj_parking(self):
        # Test Bike Facility and Parking Lane Width Filter
        self.BicycleFacilityWidth = None
        self.ParkingLaneWidth = None
        self.assertEqual(calculate_bikelane_with_adj_parking(self), 99)
        self.BicycleFacilityWidth = 1
        self.assertEqual(calculate_bikelane_with_adj_parking(self), 99)

        # Test 1 Lane Per Direction or No lanes per direction
        LanesPerDirection = [None, 1]
        for l in LanesPerDirection:
            self.LanesPerDirection = l
            IDOTAADT = [None, 1500, 3500, 50000]
            BicycleFacility = [10, 7, 4]
            ParkingLaneWidth = [6, 7, 4]
            score_matrix = [[1, 2, 3],
                            [1, 2, 3],
                            [2, 3, 3],
                            [2, 4, 4]]
            outer_list = []
            inner_list = []
            for i in IDOTAADT:
                self.IDOTAADT = i
                for (b, p) in zip(BicycleFacility, ParkingLaneWidth):
                    self.BicycleFacilityWidth = b
                    self.ParkingLaneWidth = p
                    score = calculate_bikelane_with_adj_parking(self)
                    inner_list.append(score)
                outer_list.append(inner_list)
                inner_list = []

            self.assertEqual(outer_list, score_matrix)

        # Test 2 Lane Per Direction
        self.LanesPerDirection = 2
        IDOTAADT = [500, 3000, 30000, 30001]
        BicycleFacility = [10, 7]
        ParkingLaneWidth = [5, 7]
        score_matrix = [[2, 3],
                        [2, 3],
                        [3, 3],
                        [3, 4]]
        outer_list = []
        inner_list = []
        for i in IDOTAADT:
            self.IDOTAADT = i
            for (b, p) in zip(BicycleFacility, ParkingLaneWidth):
                self.BicycleFacilityWidth = b
                self.ParkingLaneWidth = p
                score = calculate_bikelane_with_adj_parking(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_bike_lane_without_adj_parking(self):
        # Test Bicycle Facility Filter
        self.BicycleFacilityWidth = None
        self.assertEqual(calculate_bikelane_without_adj_parking(self), 99)

        # Test 1 Lane Per Direction or None
        LanesPerDirection = [None, 1]
        for l in LanesPerDirection:
            self.LanesPerDirection = l
            IDOTAADT = [None, 30000, 40000]
            BicycleFacilityWidth = [7, 5.5, 4]
            score_matrix = [[1, 1, 2],
                            [2, 3, 3],
                            [3, 4, 4]]
            outer_list = []
            inner_list = []
            for i in IDOTAADT:
                self.IDOTAADT = i
                for b in BicycleFacilityWidth:
                    self.BicycleFacilityWidth = b
                    score = calculate_bikelane_without_adj_parking(self)
                    inner_list.append(score)
                outer_list.append(inner_list)
                inner_list = []

            self.assertEqual(outer_list, score_matrix)

        # Test more than 1 lane per direction
        self.LanesPerDirection = 3
        IDOTAADT = [3000, 30000, 30001]
        BicycleFacilityWidth = [7, 6]
        score_matrix = [[1, 3],
                        [2, 3],
                        [3, 4]]
        outer_list = []
        inner_list = []
        for i in IDOTAADT:
            self.IDOTAADT = i
            for b in BicycleFacilityWidth:
                self.BicycleFacilityWidth = b
                score = calculate_bikelane_without_adj_parking(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_right_turn_lane(self):
        self.LaneConfiguration = None
        self.RightTurnLength = 0
        self.BikeLaneApproachAlignment = None
        self.rightTurnLaneScore = 0

        # Test No Lane Configuration
        self.assertEqual(calculate_right_turn_lane(self), 0)

        # Test condition 1
        self.LaneConfiguration = "XXTR"
        self.RightTurnLength = 120
        self.BikeApproachAlignment = "Straight"
        self.assertEqual(calculate_right_turn_lane(self), 2)

        # Test Condition 2
        self.LaneConfiguration = "XXLTTR"
        self.RightTurnLength = 151
        self.BikeApproachAlignment = "Straight"
        self.assertEqual(calculate_right_turn_lane(self), 3)

        # Test Condition 3
        self.LaneConfiguration = "XXLTTR"
        self.RightTurnLength = 151
        self.BikeApproachAlignment = "Left"
        self.assertEqual(calculate_right_turn_lane(self), 3)

        # Test Condition 4
        self.LaneConfiguration = "XXLTTQ"
        self.RightTurnLength = 151
        self.BikeApproachAlignment = "Straight"
        self.assertEqual(calculate_right_turn_lane(self), 4)

        self.LaneConfiguration = "XXTR"
        self.RightTurnLength = 120
        self.BikeApproachAlignment = "Straight"
        self.assertEqual(calculate_right_turn_lane(self), 2)

    def test_left_turn_lane(self):
        self.LaneConfiguration = None
        self.PostedSpeed = 0
        self.leftTurnLaneScore = 0
        self.dummy = 10

        self.assertEqual(calculate_left_turn_lane(self), 0)

        # Test for dual shared or exclusive left turn lane
        self.LaneConfiguration = "XXLTTR"
        self.assertEqual(calculate_left_turn_lane(self), 4)
        self.LaneConfiguration = "XXKTTR"
        self.assertEqual(calculate_left_turn_lane(self), 4)

        # Test for Lanecrossed criterias
        self.LaneConfiguration = "XXTTR"
        self.PostedSpeed = 25
        self.lanecrossed = 0


        lanecrossed = [0, 1, 2]
        posted_speed = [25, 30, 35]
        score_matrix = [[2, 2, 3],
                        [2, 3, 4],
                        [3, 4, 4]]
        outer_list = []
        inner_list = []
        for p in posted_speed:
            self.PostedSpeed = p
            for l in lanecrossed:
                self.lanecrossed = l
                score = calculate_left_turn_lane(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_unsignalized_crossing_without_median(self):
        self.LaneConfiguration = "XXTT"
        self.PostedSpeed = 25
        self.totalLanes = 3
        self.assertEqual(calculate_unsignalized_crossing_without_median(
            self), 1)

        posted_speed = [25, 30, 35, 40]
        total_lanes = [3, 5, 6]
        score_matrix = [[1, 2, 4],
                        [1, 2, 4],
                        [2, 3, 4],
                        [3, 4, 4]]
        outer_list = []
        inner_list = []
        for p in posted_speed:
            self.PostedSpeed = p
            for l in total_lanes:
                self.totalLanes = l
                score = calculate_unsignalized_crossing_without_median(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []
        self.assertEqual(outer_list, score_matrix)

    def test_unsignalized_crossing_with_median(self):
        self.LaneConfiguration = "XXTT"
        posted_speed = [25, 30, 35, 40]
        max_lanes = [2, 3, 4]
        score_matrix = [[1, 1, 2],
                        [1, 2, 3],
                        [2, 3, 4],
                        [3, 4, 4]]
        outer_list = []
        inner_list = []
        for p in posted_speed:
            self.PostedSpeed = p
            for m in max_lanes:
                self.maxLane = m
                score = calculate_unsignalized_crossing_with_median(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []
        self.assertEqual(outer_list, score_matrix)

    def test_max_lane(self):
        self.assertEqual(calculate_max_lane(self, 'XXTT'), 2)
        self.assertEqual(calculate_max_lane(self, 'TT'), 2)
        self.assertEqual(calculate_max_lane(self, 'XXX'), 3)
        self.assertEqual(calculate_max_lane(self, 'XXLTTR'), 4)
        self.assertEqual(calculate_max_lane(self, 'XXXXTR'), 4)
        self.assertEqual(calculate_max_lane(self, None), 1)

    def test_lane_crossed(self):
        self.assertEqual(calculate_lanecrossed(self, None), 0)
        self.assertEqual(calculate_lanecrossed(self, 'X'), 0)
        self.assertEqual(calculate_lanecrossed(self, 'T'), 0)
        self.assertEqual(calculate_lanecrossed(self, 'XT'), 0)
        self.assertEqual(calculate_lanecrossed(self, 'XXTT'), 1)
        self.assertEqual(calculate_lanecrossed(self, 'XXLTR'), 2)
        self.assertEqual(calculate_lanecrossed(self, 'XXXXLLTR'), 3)
        self.assertEqual(calculate_lanecrossed(self, 'XXXLLTTR'), 4)

    def test_aggregate_score(self):
        self.assertEqual(aggregate_score(1, 2, 3, method="MAX"), 3)
        self.assertEqual(aggregate_score(1, 4, 3, 1, method="MAX"), 4)
        self.assertEqual(aggregate_score(4, 3, 1, method="MIN"), 1)
        self.assertEqual(aggregate_score(2, 4, 3, 2, method="MIN"), 2)

    def test_blts(self):
        # Write a test for blts method
        pass


class TestPLTS(unittest.TestCase):
    dummy = 1
    dummy_2 = None
    dummy_3 = True

    def test_evironment_setup(self):
        self.assertTrue(self.dummy_3)
        self.assertEqual(self.dummy, 1)
        self.assertTrue(self.dummy_2 is None)

    def test_sidewalk_conditions(self):
        sidewalk_width = [3, 4, 5, 6]
        sidewalk_cond = ["Good", "Fair", "Poor", "Terrible"]
        score_matrix = [[4, 4, 4, 4],
                        [3, 3, 3, 4],
                        [2, 2, 3, 4],
                        [1, 1, 2, 3]]
        outer_list = []
        inner_list = []
        for w in sidewalk_width:
            self.sidewalk_width = w
            for c in sidewalk_cond:
                self.sidewalk_cond = c
                score = calculate_sidewalk_conditions(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []
        self.assertEqual(outer_list, score_matrix)

    def test_physical_buffer(self):
        buffer_type = ["No Buffer", "Solid Buffer", "Landscaped", "Vertical"]
        posted_speed = [25, 30, 35, 40]
        score_matrix = [[2, 3, 3, 4],
                        [2, 2, 2, 2],
                        [1, 2, 2, 2],
                        [1, 1, 1, 2]]
        outer_list = []
        inner_list = []
        for b in buffer_type:
            self.buffer_type = b
            for p in posted_speed:
                self.PostedSpeed = p
                score = calculate_physical_buffer(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []
        self.assertEqual(outer_list, score_matrix)

    def test_total_buffering_width(self):
        total_lanes = [2, 3, 5, 6]
        buffer_width = [4, 7, 12, 24, 25]
        score_matrix = [[2, 2, 1, 1, 1],
                        [3, 2, 2, 1, 1],
                        [4, 3, 2, 1, 1],
                        [4, 4, 3, 2, 2]]
        outer_list = []
        inner_list = []
        for l in total_lanes:
            self.TotalLanes = l
            for w in buffer_width:
                self.buffer_width = w
                score = calculate_total_buffering_width(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []
        self.assertEqual(outer_list, score_matrix)

    def test_general_landuse(self):
        self.general_landuse = "residential"
        self.assertEqual(calculate_general_landuse(self), 1)
        self.general_landuse = "strip commerical"
        self.assertEqual(calculate_general_landuse(self), 2)
        self.general_landuse = "big-box"
        self.assertEqual(calculate_general_landuse(self), 3)
        self.general_landuse = "freeway interchages"
        self.assertEqual(calculate_general_landuse(self), 4)
        self.general_landuse = "school"
        self.assertEqual(calculate_general_landuse(self), 0)

    def test_convert_score(self):
        self.assertEqual(convert_score(self, 91), 'Good')
        self.assertEqual(convert_score(self, 90), 'Good')
        self.assertEqual(convert_score(self, 80), 'Fair')
        self.assertEqual(convert_score(self, 70), 'Poor')
        self.assertEqual(convert_score(self, 60), 'Very Poor')
        self.assertEqual(convert_score(self, None), 'Very Poor')

    def test_convert_feet_to_inches(self):
        self.assertEqual(convert_feet_to_inches(self, 12), 1)
        self.assertEqual(convert_feet_to_inches(self, 45), 3.75)
        self.assertEqual(convert_feet_to_inches(self, None), 0)

    def test_calculate_total_lanes_crossed(self):
        self.MarkedCenterLine = "No"
        self.assertEqual(calculate_total_lanes_crossed(self, None), 1)
        self.MarkedCenterLine = "No"
        self.assertEqual(calculate_total_lanes_crossed(self, "XT"), 2)

        self.MarkedCenterLine = "Yes"
        self.assertEqual(calculate_total_lanes_crossed(self, None), 2)
        self.MarkedCenterLine = "Yes"
        self.assertEqual(calculate_total_lanes_crossed(self, "XXTT"), 4)

    def test_categorized_functional_class(self):
        self.assertEqual(categorize_functional_class(self, 1), "A")
        self.assertEqual(categorize_functional_class(self, 3), "A")
        self.assertEqual(categorize_functional_class(self, 4), "C")
        self.assertEqual(categorize_functional_class(self, None), "C")

    def test_calculate_unsignalized_collector_crossing_score(self):
        PostedSpeed = [20, 30, 35, 40]
        total_lanes_crossed = [1, 2]
        score_matrix = [[1, 1],
                        [1, 2],
                        [2, 2],
                        [3, 3]]
        outer_list = []
        inner_list = []
        for s in PostedSpeed:
            self.PostedSpeed = s
            for l in total_lanes_crossed:
                self.lanecrossed = l
                score = calculate_unsignalized_collector_crossing_score(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []
        self.assertEqual(outer_list, score_matrix)


if __name__ == '__main__':
    unittest.main()
