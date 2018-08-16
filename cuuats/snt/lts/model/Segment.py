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
            return 99

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

    def _calculate_right_turn_lane(self, approach):
        if approach.lane_configuration is None or \
           self.functional_class is None:
            return 0

        if "R" in approach.lane_configuration:
            if approach.right_turn_lane_length <= 150 and \
               approach.bike_lane_approach is "Straight":
                return c.RTL_CRIT_TABLE[0]
            elif approach.right_turn_lane_length > 150 and \
                 approach.bike_lane_approach is "Straight":
                return c.RTL_CRIT_TABLE[1]
            else:
                return c.RTL_CRIT_TABLE[2]
        elif "Q" in approach.lane_configuration:
            return c.RTL_CRIT_TABLE[3]

        return 0

    def _calculate_left_turn_lane(self, approach):
        lane_config = approach.lane_configuration
        speed = self.posted_speed

        if lane_config is None or self.functional_class is None:
            return 0

        if "K" in lane_config or "L" in lane_config:
            table = pd.Series(c.LTL_DUAL_SHARED_TABLE)
            crit = [(speed, c.LTL_DUAL_SHARED_SPEED_SCALE)]
            return Lts.calculate_score(table, crit)
        else:
            table = pd.DataFrame(c.LTL_CRIT_TABLE)
            crit = [(speed, c.LTL_CRIT_SPEED_SCALE),
                    (speed, c.LTL_CRIT_LANE_CROSSED_SCALE)]
            return Lts.calculate_score(table, crit)

    def blts_score(self, approaches, bike_paths=None, turn_threshold=0):
        rtl_score = 0
        ltl_score = 0

        if bike_paths is None:
            segment_score = self._calculate_mix_traffic()
        else:
            segment_score = Lts._aggregate_score(
                self._calculate_mix_traffic(),
                self._calculate_bikelane_with_adj_parking(bike_paths),
                self._calculate_bikelane_without_adj_parking(bike_paths),
                method='MIN'
            )

        if self.aadt >= turn_threshold:
            for approach in approaches:
                rtl_score = max(rtl_score,
                                self._calculate_right_turn_lane(approach))
                ltl_score = max(ltl_score,
                                self._calculate_left_turn_lane(approach))

        return Lts._aggregate_score(
            segment_score,
            rtl_score,
            ltl_score,
            method='MAX'
        )


if __name__ == '__main__':
    segment = Segment(bicycle_facility_width=6,
                      lanes_per_direction=2,
                      parking_lane_width=None,
                      aadt=3001,
                      functional_class='Major',
                      posted_speed=35)
    approaches = [Approach(lane_configuration="XXTR",
                             right_turn_lane_length=160,
                             right_turn_lane_config="Single",
                             bike_lane_approach="Straight"),
                    Approach(lane_configuration="XXLT",
                             right_turn_lane_length=151,
                             right_turn_lane_config="Dual",
                             bike_lane_approach="Left")]
    bike_paths = [BikePath(width=8)]
    print(segment.blts_score(approaches, bike_paths))
