## postgis blts class
from cuuats.snt.lts.lts_postgis import Lts
from cuuats.snt.lts.Segment import Segment
from cuuats.snt.lts.Approach import Approach
from cuuats.snt.lts import config as c

class Blts(Lts):
    def __init__(self, **kwargs):
        self.segment = kwargs.get('segment')
        self.approaches = []
        for a in kwargs.get('approaches'):
            self.approaches.append(a)
        self.intersections = []
        # for i in kwargs.get('intersections'):
        #     self.intersections.append(i)

        self.calculate_turn = self._turn_criteria_check(kwargs.get('turn_criteria'))

        self.bike_lane_with_adj_parking_score = 0
        self.bike_lane_without_adj_parking_score = 0
        self.right_turn_lane_score = 0
        self.left_turn_lane_score = 0
        self.mix_traffic_score = 0
        self.blts_score = 0

    def _turn_criteria_check(self, turn_criteria):
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
        if self.calculate_turn:
            for approach in self.approaches:
                self.approach = approach
                self._calculate_right_turn_lane()
                self._calculate_left_turn_lane()

        self.blts_score = self._aggregate_score(
            self.right_turn_lane_score,
            self.left_turn_lane_score,
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
    print(blts.segment_score)
    import pdb; pdb.set_trace()
