## postgis blts class
from cuuats.snt.lts.lts_postgis import Lts
from cuuats.snt.lts import config as c

class Blts(Lts):
    def __init__(self, **kwargs):
        self.bicycle_facility_type = kwargs.get('bicycle_facility_type')
        self.bicycle_facility_width = kwargs.get('bicycle_facility_width')
        self.lanes_per_direction = kwargs.get('lanes_per_direction')
        self.parking_lane_width = kwargs.get('parking_lane_width')
        self.idot_aadt = kwargs.get('idot_aadt')

        self.bike_lane_with_adj_parking_score = 0
        self.bike_lane_without_adj_parking_score = 0
        self.mix_traffic_score = 0

    def _calculate_bikelane_with_adj_parking(self):
        score = 0
        if self.bicycle_facility_width is not None and \
            self.parking_lane_width is not None:
            if self.lanes_per_direction is 1 or self.lanes_per_direction is None:
                score = self._calculate_score(
                    c.BL_ADJ_PK_TABLE_ONE_LANE,
                    ['self.idot_aadt <= 1000 or self.idot_aadt is None',
                     'self.idot_aadt <= 3000',
                     'self.idot_aadt <= 30000',
                     'True'],
                    ['self.bicycle_facility_width + self.parking_lane_width >= 15',
                     'self.bicycle_facility_width + self.parking_lane_width > 13',
                     'True'])
            else:
                score = self._calculate_score(
                    c.BL_ADJ_PK_TABLE_TWO_LANES,
                    ['self.idot_aadt <= 1000 or self.idot_aadt is None',
                     'self.idot_aadt <= 3000',
                     'self.idot_aadt <= 30000',
                     'True'],
                    ['self.bicycle_facility_width + '
                     'self.parking_lane_width >= 15',
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
        if self.bicycle_facility_width is not None:
            if self.lanes_per_direction is 1 or self.lanes_per_direction is None:
                score = self._calculate_score(
                    c.BL_NO_ADJ_PK_TABLE_ONE_LANE,
                    ['self.idot_aadt <= 3000 or self.idot_aadt is None',
                     'self.idot_aadt <= 30000',
                     'True'],
                    ['self.bicycle_facility_width >= 7',
                     'self.bicycle_facility_width >= 5.5',
                     'True'])
            else:
                score = self._calculate_score(
                    c.BL_NO_ADJ_PK_TABLE_TWO_LANES,
                    ['self.idot_aadt <= 3000 or self.idot_aadt is None',
                     'self.idot_aadt <= 30000',
                     'True'],
                    ['self.bicycle_facility_width >= 7',
                     'True'])

        self.bike_lane_without_adj_parking_score = score
        return(score)

    def calculate_mix_traffic(self):
        """
        this function calculate the mix traffic scores based on the specify
        criterias
        :param self: self
        :return: int score
        """
        score = 0
        score = calculate_score(
            self,
            c.MIXED_TRAF_TABLE,
            ['self.idot_aadt <= 1000',
             'self.idot_aadt <= 3000',
             'True'],
            ['self.lanes_per_direction in (0, None)',
             'self.lanes_per_direction == 1',
             'self.lanes_per_direction == 2',
             'self.lanes_per_direction >= 3'])

        self.mix_traffic_score = score
        return(score)

    def calculate_blts(self):
        self._calculate_bikelane_with_adj_parking()
        self._calculate_bikelane_without_adj_parking()
        self.segment_score = self._aggregate_score(
            self.bike_lane_with_adj_parking_score,
            self.bike_lane_without_adj_parking_score,
            self.mix_traffic_score,
            method = "MIN"
        )



blts = Blts(bicycle_facility_width = 6, lanes_per_direction = 1, parking_lane_width = 10, idot_aadt = 5000)
blts.calculate_blts()
print(blts.segment_score)
