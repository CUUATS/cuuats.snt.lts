# Segment Class for LTS Assessment
from cuuats.snt.lts import config as c
from cuuats.snt.lts.lts_postgis import Lts
from cuuats.snt.lts.model.Approach import Approach
from cuuats.snt.lts.model.BikePath import BikePath
from cuuats.snt.lts.model.Sidewalk import Sidewalk


class Segment(object):
    def __init__(self, **kwargs):
        self.lanes_per_direction = Lts.remove_none(
                                    kwargs.get('lanes_per_direction'))
        self.parking_lane_width = kwargs.get('parking_lane_width')
        self.aadt = int(Lts.remove_none(kwargs.get('aadt')))
        self.functional_class = self._categorize_functional_class(
                                    Lts.remove_none(
                                        kwargs.get('functional_class')))
        self.posted_speed = Lts.remove_none(kwargs.get('posted_speed'))
        self.total_lanes = Lts.remove_none(kwargs.get('total_lanes'))
        self.marked_center_lane = kwargs.get('marked_center_lane')
        self.overall_landuse = kwargs.get('overall_landuse')

    def _categorize_functional_class(self, functional_class):
        if functional_class is None:
            return "C"
        if functional_class >= 4:
            return "C"
        else:
            return "A"

    def _find_off_street_trail(self, bike_path):
        trail = c.OFF_STREET_TRAIL
        if trail.get(bike_path.path_category) == 'Off-Street Trail':
            return True
        return False

    def _calculate_mix_traffic(self):
        """
        this function calculate the mix traffic scores based on the specify
        criterias
        :param self: self
        :return: np.int64 score
        """
        aadt = self.aadt
        lpd = Lts.remove_none(self.lanes_per_direction)
        table = c.MIXED_TRAF_TABLE
        aadt_scale = c.URBAN_FIX_TRAFFIC_AADT_SCALE
        lane_scale = c.URBAN_FIX_TRAFFIC_LANE_SCALE

        crits = ([aadt, aadt_scale],
                 [lpd, lane_scale])
        return Lts.calculate_score(table, crits)

    def _calculate_bikelane_with_adj_parking(self, bike_path):
        parking_lane_width = self.parking_lane_width
        lpd = self.lanes_per_direction
        aadt = self.aadt
        one_lane_table = c.BL_ADJ_PK_TABLE_ONE_LANE
        multi_lane_table = c.BL_ADJ_PK_TABLE_TWO_LANES
        aadt_scale = c.BL_ADJ_PK_AADT_SCALE
        width_scale = c.BL_ADJ_PK_WIDTH_SCALE
        width_scale_two_lanes = c.BL_ADJ_PK_TWO_WIDTH_SCALE
        width = bike_path.width

        score = float('Inf')
        # if there is no bike lane width or no bike lane
        if parking_lane_width is None or width is None:
            return score

        # No marked lanes or 1 lpd
        elif lpd is None or lpd == 1:
            crits = ([aadt, aadt_scale],
                     [width + parking_lane_width, width_scale])
            return Lts.calculate_score(one_lane_table, crits)
        # 2 lpd or greater
        else:
            crits = ([aadt, aadt_scale],
                     [width + parking_lane_width, width_scale_two_lanes])
            return Lts.calculate_score(multi_lane_table, crits)

    def _calculate_bikelane_without_adj_parking(self, bike_path):
        parking_lane_width = self.parking_lane_width
        lpd = self.lanes_per_direction
        aadt = self.aadt
        one_lane_table = c.BL_NO_ADJ_PK_TABLE_ONE_LANE
        multi_lane_table = c.BL_NO_ADJ_PK_TABLE_TWO_LANES
        aadt_scale = c.BL_NO_ADJ_PK_AADT_SCALE
        width_scale_one_lane = c.BL_NO_ADJ_PK_WIDTH_SCALE
        width_scale_two_lane = c.BL_NO_ADJ_PK_TWO_WIDTH_SCALE
        width = bike_path.width

        score = 99
        if parking_lane_width is not None or width is None:
            return score
        # no marked lane or 1 lpd
        elif lpd is None or lpd == 1:
            crits = ([aadt, aadt_scale],
                     [width, width_scale_one_lane])
            return Lts.calculate_score(one_lane_table, crits)
        # 2 lps or greater
        else:
            crits = ([aadt, aadt_scale],
                     [width, width_scale_two_lane])
            return Lts.calculate_score(multi_lane_table, crits)

    def _calculate_right_turn_lane(self, approach):
        lane_config = approach.lane_configuration
        rtl_length = approach.right_turn_lane_length
        bike_lane_approach = approach.bike_lane_approach
        functional_class = self.functional_class
        rtl_score = c.RTL_CRIT_TABLE
        straight = "Straight"
        R = "R"  # right turn lane
        Q = "Q"  # dual shared right turn

        score = 0
        if lane_config is None or functional_class == "C":
            return score

        if R in lane_config:
            if rtl_length <= 150 and bike_lane_approach is straight:
                return rtl_score[0]
            elif rtl_length > 150 and bike_lane_approach is straight:
                return rtl_score[1]
            else:
                return rtl_score[2]
        elif Q in lane_config:
            return rtl_score[3]

        return score

    def _calculate_left_turn_lane(self, approach):
        lane_config = approach.lane_configuration
        speed = self.posted_speed
        functional_class = self.functional_class
        K = "K"  # dual shared
        L = "L"  # exclusive left turn lane
        dual_share_table = c.LTL_DUAL_SHARED_TABLE
        ltl_table = c.LTL_CRIT_TABLE
        lane_crossed = Lts.calculate_ltl_crossed(lane_config)
        speed_scale = c.LTL_DUAL_SHARED_SPEED_SCALE
        lane_crossed_scale = c.LTL_CRIT_LANE_CROSSED_SCALE

        if lane_config is None or functional_class == "C":
            return 0
        if L in lane_config or K in lane_config:
            crit = [(speed, speed_scale)]
            return Lts.calculate_score(dual_share_table, crit)
        else:
            crit = [(speed, speed_scale),
                    (lane_crossed, lane_crossed_scale)]

            return Lts.calculate_score(ltl_table, crit)

    def _calculate_condition_score(self, sidewalk):
        width = sidewalk.sidewalk_width
        cond = sidewalk.sidewalk_score
        table = c.SW_COND_TABLE
        width_scale = c.SW_COND_WIDTH_SCALE
        cond_scale = c.SW_COND_COND_SCALE
        no_sidewalk_score = 4

        # PLTS 4 if there is no sidewalk
        if width is None or cond is None:
            return no_sidewalk_score

        crits = ([width, width_scale],
                 [cond, cond_scale])

        return Lts.calculate_score(table, crits)

    def _calculate_buffer_type_score(self, sidewalk):
        buffer_type = c.BUFFER_TYPE_DICT.get(sidewalk.buffer_type)
        speed = self.posted_speed
        table = c.BUFFER_TYPE_TABLE
        buffer_scale = c.BUFFER_TYPE_TYPE_SCALE
        speed_scale = c.BUFFER_TYEP_SPEED_SCALE

        crits = ([buffer_type, buffer_scale],
                 [speed, speed_scale])

        return Lts.calculate_score(table, crits)

    def _calculate_buffer_width_score(self, sidewalk):
        total_lanes = self.total_lanes
        buffer_width = sidewalk.buffer_width
        width_scale = c.BUFFER_WIDTH_WIDTH_SCALE
        lane_scale = c.BUFFER_WIDTH_LANE_SCALE
        table = c.BUFFER_WIDTH_TABLE
        crits = ([total_lanes, lane_scale],
                 [buffer_width, width_scale])

        return Lts.calculate_score(table, crits)

    def _calculate_landuse_score(self):
        # method to get landuse score from a dictionary
        # return c.LANDUSE_DICT.get(self.overall_landuse)

        # return the overall value in database as score
        if self.overall_landuse == '0':
            return 1
        return int(self.overall_landuse)

    def blts_score(self, approaches, bike_paths=None, turn_threshold=0):
        rtl_score = 0
        ltl_score = 0
        pk_score = 0
        no_pk_score = 0

        mix_traffic_score = self._calculate_mix_traffic()

        for bike_path in bike_paths:
            if self._find_off_street_trail(bike_path):
                return c.OFF_STREET_TRAIL_SCORE

            pk_score = max(pk_score,
                           self._calculate_bikelane_with_adj_parking(
                            bike_path))
            no_pk_score = max(pk_score,
                              self._calculate_bikelane_without_adj_parking(
                               bike_path))

        segment_score = Lts.aggregate_score(
            mix_traffic_score,
            pk_score,
            no_pk_score,
            method='MIN'
        )

        if self.aadt >= turn_threshold:
            for approach in approaches:
                rtl_score = max(rtl_score,
                                self._calculate_right_turn_lane(approach))
                ltl_score = max(ltl_score,
                                self._calculate_left_turn_lane(approach))

        return Lts.aggregate_score(
            segment_score,
            rtl_score,
            ltl_score,
            method='MAX'
        )

    def plts_score(self, sidewalks=None):
        segment_score = float('Inf')
        for sidewalk in sidewalks:
            cond_score = self._calculate_condition_score(sidewalk)
            # buffer_type_score = self._calculate_buffer_type_score(sidewalk)
            buffer_width_score = self._calculate_buffer_width_score(sidewalk)
            landuse_score = self._calculate_landuse_score()
            sidewalk_score = max(cond_score,
                                 # buffer_type_score,
                                 buffer_width_score,
                                 landuse_score)

            segment_score = min(segment_score, sidewalk_score)

        return segment_score


if __name__ == '__main__':
    segment = Segment(lanes_per_direction=None,
                      parking_lane_width=5,
                      aadt=None,
                      functional_class=None,
                      posted_speed=35,
                      total_lanes=6)
    approaches = [Approach(lane_configuration=None,
                           right_turn_lane_length=None,
                           bike_lane_approach=None)]
    bike_paths = [BikePath(width=1)]
    print(segment.blts_score(approaches, bike_paths))

    sidewalks = [(Sidewalk(sidewalk_width=5,
                           sidewalk_score=65,
                           buffer_type='solid_surface',
                           buffer_width=20,
                           overall_landuse=1))]

    print(segment.plts_score(sidewalks))
