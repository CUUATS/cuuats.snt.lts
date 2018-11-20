# Segment Class for LTS Assessment
from cuuats.snt.lts import config as c
from cuuats.snt.lts import utils


class Segment(object):
    def __init__(self, **kwargs):
        self.lanes_per_direction = kwargs.get('lanes_per_direction') or 0
        self.parking_lane_width = kwargs.get('parking_lane_width')
        self.aadt = int(kwargs.get('aadt') or 0)
        self.functional_class = self._categorize_functional_class(
            kwargs.get('functional_class') or 0)
        self.interstate = self._is_interstate(kwargs.get('functional_class'))
        self.posted_speed = kwargs.get('posted_speed') or 0
        self.total_lanes = kwargs.get('total_lanes') or 0
        self.marked_center_lane = kwargs.get('marked_center_lane')
        self.overall_landuse = kwargs.get('overall_landuse')

    def _is_interstate(self, functional_class):
        if functional_class == 1:
            return True
        return False

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
        lpd = self.lanes_per_direction
        table = c.MIXED_TRAF_TABLE
        aadt_scale = c.URBAN_FIX_TRAFFIC_AADT_SCALE
        lane_scale = c.URBAN_FIX_TRAFFIC_LANE_SCALE

        crits = ([aadt, aadt_scale],
                 [lpd, lane_scale])
        return utils.calculate_score(table, crits)

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
            return utils.calculate_score(one_lane_table, crits)
        # 2 lpd or greater
        else:
            crits = ([aadt, aadt_scale],
                     [width + parking_lane_width, width_scale_two_lanes])
            return utils.calculate_score(multi_lane_table, crits)

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
        buffer_width = bike_path.buffer_width

        score = 99
        if parking_lane_width is not None or width is None:
            return score
        # no marked lane or 1 lpd
        elif lpd is None or lpd == 1:
            crits = ([aadt, aadt_scale],
                     [width + buffer_width, width_scale_one_lane])
            return utils.calculate_score(one_lane_table, crits)
        # 2 lps or greater
        else:
            crits = ([aadt, aadt_scale],
                     [width + buffer_width, width_scale_two_lane])
            return utils.calculate_score(multi_lane_table, crits)

    def _calculate_right_turn_lane(self, approach):
        lane_config = approach.lanes.config
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
        speed = self.posted_speed
        functional_class = self.functional_class
        K = "K"  # dual shared
        L = "L"  # exclusive left turn lane
        dual_share_table = c.LTL_DUAL_SHARED_TABLE
        ltl_table = c.LTL_CRIT_TABLE
        lane_crossed = approach.lanes.lanes_crossed
        speed_scale = c.LTL_DUAL_SHARED_SPEED_SCALE
        lane_crossed_scale = c.LTL_CRIT_LANE_CROSSED_SCALE

        if approach.lanes.config is None or functional_class == "C":
            return 0
        if L in approach.lanes.config or K in approach.lanes.config:
            crit = [(speed, speed_scale)]
            return utils.calculate_score(dual_share_table, crit)
        else:
            crit = [(speed, speed_scale),
                    (lane_crossed, lane_crossed_scale)]

            return utils.calculate_score(ltl_table, crit)

    def _calculate_crossing_without_median(self, crossing):
        speed = crossing.crossing_speed
        lanes_crossed = crossing.lanes
        crossing_no_med_table = c.CROSSING_NO_MED_TABLE
        speed_scale = c.CROSSING_NO_MED_SPEED_SCALE
        lane_scale = c.CROSSING_NO_MED_LANE_SCALE

        crit = [(speed, speed_scale),
                (lanes_crossed, lane_scale)]

        return utils.calculate_score(crossing_no_med_table, crit)

    def _calculate_crossing_with_median(self, crossing):
        speed = crossing.crossing_speed
        lanes_crossed = crossing.lanes
        crossing_no_med_table = c.CROSSING_NO_MED_TABLE
        speed_scale = c.CROSSING_HAS_MED_SPEED_SCALE
        lane_scale = c.CROSSING_HAS_MED_LANE_SCALE

        crit = [(speed, speed_scale),
                (lanes_crossed, lane_scale)]

        return utils.calculate_score(crossing_no_med_table, crit)

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

        return utils.calculate_score(table, crits)

    def _calculate_buffer_type_score(self, sidewalk):
        buffer_type = c.BUFFER_TYPE_DICT.get(sidewalk.buffer_type, 'no buffer')
        speed = self.posted_speed
        table = c.BUFFER_TYPE_TABLE
        buffer_scale = c.BUFFER_TYPE_TYPE_SCALE
        speed_scale = c.BUFFER_TYEP_SPEED_SCALE

        crits = ([buffer_type, buffer_scale],
                 [speed, speed_scale])

        return utils.calculate_score(table, crits)

    def _calculate_buffer_width_score(self, sidewalk):
        total_lanes = self.total_lanes
        buffer_width = sidewalk.buffer_width
        width_scale = c.BUFFER_WIDTH_WIDTH_SCALE
        lane_scale = c.BUFFER_WIDTH_LANE_SCALE
        table = c.BUFFER_WIDTH_TABLE
        crits = ([total_lanes, lane_scale],
                 [buffer_width, width_scale])

        return utils.calculate_score(table, crits)

    def _calculate_landuse_score(self):
        # TODO: get landuse score from a dictionary
        # return c.LANDUSE_DICT.get(self.overall_landuse)

        # return the overall value in database as score
        if self.overall_landuse == '0':
            return 1
        return int(self.overall_landuse)

    def _calcualate_collector_crossing_wo_med(self, crossing):
        speed = crossing.crossing_speed
        lanes_crossed = crossing.lanes
        crossing_table = c.COLLECTOR_CROSSING_TABLE
        speed_scale = c.COLLECTOR_CROSSING_SPEED_SCALE
        lane_scale = c.COLLECTOR_CROSSING_LANE_SCALE

        crit = [(speed, speed_scale),
                (lanes_crossed, lane_scale)]

        return utils.calculate_score(crossing_table, crit)

    def _calculate_art_crossing_wo_med_two_lanes(self, crossing):
        speed = crossing.crossing_speed
        lanes_crossed = crossing.aadt
        crossing_table = c.ARTERIAL_CROSSING_TWO_LANES_TABLE
        speed_scale = c.ARTERIAL_CROSSING_SPEED_SCALE
        lane_scale = c.ARTERIAL_CROSSING_TWO_LANES_AADT_SCALE

        crit = [(speed, speed_scale),
                (lanes_crossed, lane_scale)]

        return utils.calculate_score(crossing_table, crit)

    def _calculate_art_crossing_wo_med_three_lanes(self, crossing):
        speed = crossing.crossing_speed
        lanes_crossed = crossing.aadt
        crossing_table = c.ARTERIAL_CROSSING_THREE_LANES_TABLE
        speed_scale = c.ARTERIAL_CROSSING_SPEED_SCALE
        lane_scale = c.ARTERIAL_CROSSING_THREE_LANES_AADT_SCALE

        crit = [(speed, speed_scale),
                (lanes_crossed, lane_scale)]

        return utils.calculate_score(crossing_table, crit)

    def _vertical_score(self, bike_path, score):
        if bike_path.buffer_type == c.VERTICAL_TRAIL:
            if score is float('Inf'):
                return score
            elif score > 1:
                return score - 1
        return score

    def _calculate_on_street_path_score(self, bike_path):
        category = bike_path.path_category
        buffer_width = bike_path.buffer_width
        path_type = bike_path.path_type

        on_street = 'On-Street Bikeway'
        sharrows = 'Sharrows'

        if category != on_street:
            return c.ON_STREET_FACILITY.get('no_facility')

        if buffer_width > 0:
            return c.ON_STREET_FACILITY.get('buffered')

        if path_type != sharrows:
            return c.ON_STREET_FACILITY.get('non_buffered')

        return c.ON_STREET_FACILITY.get('sharrows')

    def alts_score(self, bike_paths=None):
        segment_score = 1
        for bike_path in bike_paths:
            path_score = self._calculate_on_street_path_score(bike_path)

        return max(segment_score, path_score)

    def blts_score(self, approaches, crossings,
                   bike_paths=None, turn_threshold=0):

        # Interstate Score
        if self.interstate:
            return 4

        rtl_score = 0
        ltl_score = 0
        pk_score = 0
        no_pk_score = 0

        mix_traffic_score = self._calculate_mix_traffic()

        for bike_path in bike_paths:
            if self._find_off_street_trail(bike_path):
                return c.OFF_STREET_TRAIL_SCORE

            # adds vertical logic
            p = self._vertical_score(
                bike_path,
                self._calculate_bikelane_with_adj_parking(
                  bike_path)
            )
            pk_score = max(pk_score, p)

            # adds vertical logic
            n = self._vertical_score(
                bike_path,
                self._calculate_bikelane_without_adj_parking(
                    bike_path)
            )
            no_pk_score = max(no_pk_score, n)

        segment_components = [
            mix_traffic_score,
            pk_score,
            no_pk_score
        ]

        segment_score = min([s for s in segment_components if s is not 0])

        if self.aadt >= turn_threshold:
            # turn lane criteria
            for approach in approaches:
                rtl_score = max(rtl_score,
                                self._calculate_right_turn_lane(approach))
                ltl_score = max(ltl_score,
                                self._calculate_left_turn_lane(approach))

        # crossing criteria
        for crossing in crossings:
            if crossing.control_type == 'Signal':
                crossing_score = 1
            else:
                if crossing.median is None:
                    crossing_score = self._calculate_crossing_without_median(
                                                        crossing)
                else:
                    crossing_score = self._calculate_crossing_with_median(
                                                        crossing)

        score_components = [
            segment_score,
            rtl_score,
            ltl_score,
            crossing_score
        ]

        return max([s for s in score_components if s is not 0])

    def plts_score(self, crossings, sidewalks=None):
        segment_score = float('Inf')
        for sidewalk in sidewalks:
            cond_score = self._calculate_condition_score(sidewalk)
            buffer_type_score = self._calculate_buffer_type_score(sidewalk)
            buffer_width_score = self._calculate_buffer_width_score(sidewalk)
            landuse_score = self._calculate_landuse_score()
            sidewalk_score = max(cond_score,
                                 buffer_type_score,
                                 buffer_width_score,
                                 landuse_score)

            segment_score = min(segment_score, sidewalk_score)
            if sidewalk.sidewalk_width is None or \
               sidewalk.sidewalk_score is None:
                return sidewalk_score
            for crossing in crossings:
                if crossing.control_type == 'Signal':
                    crossing_score = 1
                    continue
                # median criteria - no median
                if crossing.median is None:
                    # collector crossing
                    if crossing.functional_class >= 4:
                        crossing_score = \
                            self._calcualate_collector_crossing_wo_med(
                                crossing)
                    # arterial crossing
                    else:
                        if crossing.lanes <= 2:
                            crossing_score = \
                                self._calculate_art_crossing_wo_med_two_lanes(
                                    crossing
                                )
                        else:
                            crossing_score = \
                              self._calculate_art_crossing_wo_med_three_lanes(
                                    crossing
                                )
                # median criteria - median present
                else:
                    raise NotImplementedError(
                        'Can only have crossing without median')

        return max(segment_score, crossing_score)
