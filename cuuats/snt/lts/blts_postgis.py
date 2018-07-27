## postgis blts class
from cuuats.snt.lts.lts_postgis import Lts
from cuuats.snt.lts.model.Segment import Segment
from cuuats.snt.lts.model.Approach import Approach
from cuuats.snt.lts import config as c

class Blts(Lts):
    def __init__(self, segment, approaches, turn_criteria = 10000):
        if type(segment) is Segment:
            self.segment = segment
        else:
            raise TypeError('segment is not a Segment object')

        self.approach = Approach()
        self.approaches = []
        if approaches is not None:
            for a in approaches:
                if type(a) is Approach:
                    self.approaches.append(a)
                else:
                    raise TypeError('approach is not an Approach object')

        self.calculate_turn = self._check_turn_criteria(turn_criteria)
        self.crossing_without_median_score = 0
        self.crossing_with_median_score = 0
        self.bike_lane_with_adj_parking_score = 0
        self.bike_lane_without_adj_parking_score = 0
        self.right_turn_lane_score = 0
        self.left_turn_lane_score = 0
        self.mix_traffic_score = 0
        self.blts_score = 0

    def _check_turn_criteria(self, turn_criteria):
        if self.segment is None:
            return False
        if self.segment.aadt > turn_criteria:
            return True
        else:
            return False

    def _remove_none(self, value):
        if value is None:
            value = 0
        return(value)

    def _calculate_bikelane_with_adj_parking(self):
        score = 0
        if self.segment.bicycle_facility_width is not None and \
            self.segment.parking_lane_width is not None:
            if self.segment.lanes_per_direction is 1 or self.segment.lanes_per_direction is None:
                score = self._calculate_score(
                    c.BL_ADJ_PK_TABLE_ONE_LANE,
                    ['self.segment.aadt <= 1000',
                     'self.segment.aadt <= 3000',
                     'self.segment.aadt <= 30000',
                     'True'],
                    ['self.segment.bicycle_facility_width + self.segment.parking_lane_width >= 15',
                     'self.segment.bicycle_facility_width + self.segment.parking_lane_width > 13',
                     'True'])
            else:
                score = self._calculate_score(
                    c.BL_ADJ_PK_TABLE_TWO_LANES,
                    ['self.segment.aadt <= 1000',
                     'self.segment.aadt <= 3000',
                     'self.segment.aadt <= 30000',
                     'True'],
                    ['self.segment.bicycle_facility_width + self.segment.parking_lane_width >= 15',
                     'True'])

        self.bike_lane_with_adj_parking_score = score
        return(score)

    def _calculate_bikelane_without_adj_parking(self):
        """
        This functions calculates the score of bike lanes without adjacent
        parking based on the specified criteria
        :param self: self
        :return: int score
        """
        score = 0
        if self.segment.bicycle_facility_width is not None:
            if self.segment.lanes_per_direction is 1 or self.segment.lanes_per_direction is None:
                score = self._calculate_score(
                    c.BL_NO_ADJ_PK_TABLE_ONE_LANE,
                    ['self.segment.aadt <= 3000',
                     'self.segment.aadt <= 30000',
                     'True'],
                    ['self.segment.bicycle_facility_width >= 7',
                     'self.segment.bicycle_facility_width >= 5.5',
                     'True'])
            else:
                score = self._calculate_score(
                    c.BL_NO_ADJ_PK_TABLE_TWO_LANES,
                    ['self.segment.aadt <= 3000',
                     'self.segment.aadt <= 30000',
                     'True'],
                    ['self.segment.bicycle_facility_width >= 7',
                     'True'])

        self.bike_lane_without_adj_parking_score = score
        return(score)

    def _calculate_mix_traffic(self):
        """
        this function calculate the mix traffic scores based on the specify
        criterias
        :param self: self
        :return: int score
        """
        score = 0
        score = self._calculate_score(
            c.MIXED_TRAF_TABLE,
            ['self.segment.aadt <= 1000',
             'self.segment.aadt <= 3000',
             'True'],
            ['self.segment.lanes_per_direction in (0, None)',
             'self.segment.lanes_per_direction == 1',
             'self.segment.lanes_per_direction == 2',
             'self.segment.lanes_per_direction >= 3'])

        self.mix_traffic_score = score
        return(score)

    def _calculate_right_turn_lane(self):
        score = 0
        if self.approach.lane_configuration is None or \
            self.segment.functional_class is None:
            return score

        if "R" in self.approach.lane_configuration or \
           "Q" in self.approach.lane_configuration:
            score = self._calculate_score(
                    c.RTL_CRIT_TABLE,
                    ['"R" in self.approach.lane_configuration and \
                     self.approach.right_turn_lane_length <= 150 and \
                     self.approach.bike_lane_approach is "Straight"',

                     '"R" in self.approach.lane_configuration and \
                     self.approach.right_turn_lane_length > 150 and \
                     self.approach.bike_lane_approach is "Straight"',

                     '"R" in self.approach.lane_configuration and \
                     self.approach.bike_lane_approach is "Left"',

                     'True'])
            self.right_turn_lane_score = max(self.right_turn_lane_score, score)
        return(score)

    def _calculate_left_turn_lane(self):
        """
        this function calculate the left turn lane score based on the criteria
        :param self: self
        :return: int score
        """
        score = 0
        if self.approach.lane_configuration is None or self.segment.functional_class is None:
            return score
        if "K" in self.approach.lane_configuration or "L" in self.approach.lane_configuration:
            score = self._calculate_score(
                c.LTL_DUAL_SHARED_TABLE,
                ['self.segment.posted_speed <= 25',
                 'self.segment.posted_speed == 30',
                 'self.segment.posted_speed >= 35'])
        else:
            score = self._calculate_score(
                c.LTL_CRIT_TABLE,
                ['self.segment.posted_speed <= 25',
                 'self.segment.posted_speed == 30',
                 'self.segment.posted_speed >= 35'],

                ['self.approach.lanes_crossed == 0',
                 'self.approach.lanes_crossed == 1',
                 'self.approach.lanes_crossed >= 2'])

            self.left_turn_lane_score = max(self.left_turn_lane_score, score)
        return(score)

    def _calculate_crossing_without_median(self):
        score = 0
        if self.approach.lane_configuration is None:
            return score
        score = self._calculate_score(
            c.CROSSING_NO_MED_TABLE,
            ['self.segment.posted_speed <= 25',
             'self.segment.posted_speed == 30',
             'self.segment.posted_speed == 35',
             'True'],

            ['self.approach.total_lanes <= 3',
             'self.approach.total_lanes <= 5',
             'True'])

        self.crossing_without_median_score = max(self.crossing_without_median_score, score)
        return(score)

    def _calculate_crossing_with_median(self):
        score = 0
        if self.approach.lane_configuration is None:
            return(score)

        score = self._calculate_score(
            c.CROSSING_HAS_MED_TABLE,
            ['self.segment.posted_speed <= 25',
             'self.segment.posted_speed == 30',
             'self.segment.posted_speed == 35',
             'True'],

            ['self.approach.max_lane <= 2',
             'self.approach.max_lane == 3',
             'True'])

        self.crossing_with_median_score = max(self.crossing_with_median_score, score)
        return(score)

    def calculate_blts(self):
        self._calculate_bikelane_with_adj_parking()
        self._calculate_bikelane_without_adj_parking()
        self._calculate_mix_traffic()
        self.segment_score = self._aggregate_score(
            self.bike_lane_with_adj_parking_score,
            self.bike_lane_without_adj_parking_score,
            self.mix_traffic_score,
            method = "MIN"
        )

        for approach in self.approaches:
            self.approach = approach
            if self.calculate_turn:
                self._calculate_right_turn_lane()
                self._calculate_left_turn_lane()

            if self.approach.median_present and not self.approach.is_signalized():
                self._calculate_crossing_with_median()
            else:
                self._calculate_crossing_without_median()

        self.blts_score = self._aggregate_score(
            self.right_turn_lane_score,
            self.left_turn_lane_score,
            self.crossing_without_median_score,
            self.crossing_with_median_score,
            self.segment_score,
            method = "MAX"
        )
        return(self.blts_score)


if __name__ == '__main__':
    segment = Segment(bicycle_facility_width = 6,
                        lanes_per_direction = 1,
                        parking_lane_width = 1,
                        aadt = None,
                        functional_class = 'Major',
                        posted_speed = 35)
    approaches = [Approach(lane_configuration = "XXT",
                          right_turn_lane_length = 50,
                          right_turn_lane_config = "Single",
                          bike_lane_approach = "Straight"),
                 Approach(lane_configuration = "XXT",
                           right_turn_lane_length = 151,
                           right_turn_lane_config = "Dual",
                           bike_lane_approach = "Left")]
    blts = Blts(segment=segment,
                approaches = approaches,
                turn_criteria = 10000)
    blts.calculate_blts()
    print('blts score: ' + str(blts.segment_score))
    import pdb; pdb.set_trace()
