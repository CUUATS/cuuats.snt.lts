# Segment Class for LTS Assessment
from cuuats.snt.lts import config as c
import pandas as pd
from cuuats.snt.lts.lts_postgis import Lts
from cuuats.snt.lts.model.Approach import Approach
from cuuats.snt.lts.model.BikePath import BikePath


class Segment(object):
    def __init__(self, **kwargs):
        self.bicycle_facility_type = kwargs.get('bicycle_facility_type')
        self.bicycle_facility_width = kwargs.get('bicycle_facility_width')
        self.lanes_per_direction = kwargs.get('lanes_per_direction')
        self.parking_lane_width = kwargs.get('parking_lane_width')
        self.aadt = int(self._remove_none(kwargs.get('aadt')))
        self.functional_class = kwargs.get('functional_class')
        self.posted_speed = kwargs.get('posted_speed')
        self.total_lanes = kwargs.get('total_lanes')
        self.marked_center_lane = kwargs.get('marked_center_lane')

    def _remove_none(self, value):
        if value is None:
            value = 0
        return value

    def _categorize_functional_class(self):
        if self.functional_class is None:
            return "C"
        if self.functional_class >= 4:
            return "C"
        else:
            return "A"

    def _calculate_mix_traffic(self):
        """
        this function calculate the mix traffic scores based on the specify
        criterias
        :param self: self
        :return: np.int64 score
        """
        table = pd.DataFrame(c.MIXED_TRAF_TABLE)
        crits = ([self.aadt, c.URBAN_FIX_TRAFFIC_AADT_SCALE],
                 [self.lanes_per_direction, c.URBAN_FIX_TRAFFIC_LANE_SCALE])
        return Lts.calculate_score(table, crits)

    def _calculate_bikelane_with_adj_parking(self, bike_paths):
        if self.parking_lane_width is None:
            return 0

        for bike_path in bike_paths:
            if bike_path.width is None:
                return 0

            # No marked lanes or 1 lpd
            if self.lanes_per_direction is None or \
               self.lanes_per_direction == 1:
                table = pd.DataFrame(c.BL_ADJ_PK_TABLE_ONE_LANE)
                crits = ([self.aadt, c.BL_ADJ_PK_AADT_SCALE],
                         [bike_path.width, c.BL_ADJ_PK_WIDTH_SCALE])
                return (Lts.calculate_score(table, crits))
            # 2 lpd or greater
            else:
                table = pd.DataFrame(c.BL_ADJ_PK_TABLE_TWO_LANES)
                crits = ([self.aadt, c.BL_ADJ_PK_AADT_SCALE],
                         [bike_path.width, c.BL_ADJ_PK_TWO_WIDTH_SCALE])
                return (Lts.calculate_score(table, crits))

    def _calculate_bikelane_without_adj_parking(self, bike_paths):
        if self.parking_lane_width is None:
            for bike_path in bike_paths:
                if bike_path.width is None:
                    return 0
                # no marked lane or 1 lpd
                if self.lanes_per_direction is None or \
                   self.lanes_per_direction == 1:
                    table = pd.DataFrame(c.BL_NO_ADJ_PK_TABLE_ONE_LANE)
                    crits = ([self.aadt, c.BL_NO_ADJ_PK_AADT_SCALE],
                             [bike_path.width, c.BL_NO_ADJ_PK_WIDTH_SCALE])
                    return (Lts.calculate_score(table, crits))
                # 2 lps or greater
                else:
                    table = pd.DataFrame(c.BL_NO_ADJ_PK_TABLE_TWO_LANES)
                    crits = ([self.aadt, c.BL_NO_ADJ_PK_AADT_SCALE],
                             [bike_path.width, c.BL_NO_ADJ_PK_TWO_WIDTH_SCALE])
                    return (Lts.calculate_score(table, crits))

    def blts_score(self, approaches, bike_paths):
        return Lts._aggregate_score(
            # self._calculate_mix_traffic(),
            self._calculate_bikelane_with_adj_parking(bike_paths),
            self._calculate_bikelane_without_adj_parking(bike_paths),
            method='MAX'
        )


if __name__ == '__main__':
    segment = Segment(bicycle_facility_width=6,
                      lanes_per_direction=2,
                      parking_lane_width=None,
                      aadt=3001,
                      functional_class='Major',
                      posted_speed=35)
    approaches = [Approach(lane_configuration="XXT",
                             right_turn_lane_length=50,
                             right_turn_lane_config="Single",
                             bike_lane_approach="Straight"),
                    Approach(lane_configuration="XXT",
                             right_turn_lane_length=151,
                             right_turn_lane_config="Dual",
                             bike_lane_approach="Left")]
    bike_paths = [BikePath(width=8)]
    print(segment.blts_score(approaches, bike_paths))
