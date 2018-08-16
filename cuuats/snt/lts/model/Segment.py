# Segment Class for LTS Assessment
from cuuats.snt.lts import config as c
import pandas as pd
import numpy as np
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
        score = pd.DataFrame(c.MIXED_TRAF_TABLE)
        crits = ([self.aadt, c.URBAN_FIX_TRAFFIC_SPEED_SCALE],
                 [self.lanes_per_direction, c.URBAN_FIX_TRAFFIC_LANE_SCALE])
        return self._calculate_score(score, crits)

    def _calculate_score(self, score, crits):
        if not isinstance(score, pd.DataFrame):
            raise TypeError('df argument must be a pandas dataframe object')
        assert len(crits) == 2
        for crit in crits:
            score.index = crit[1]
            score = score.loc[crit[0]]
        assert isinstance(score, np.int64)
        return score

    def _aggregate_score(self, *scores, **kwargs):
        """
        this function aggregate number of scores based on *scores
        :param self: self
        :param scores: scores arguments
        :param kwargs: "MAX" - returns maximum, "MIN" - return minimum
        :return: int score
        """
        score_list = [score for score in scores if score is not 0]
        method = kwargs.get("method")
        score = 0

        if method == "MIN":
            score = min(score_list)
        elif method == "MAX":
            score = max(score_list)
        return score

    def blts_score(self, approaches, bike_paths):
        return Lts._aggregate_score(
            self._calculate_mix_traffic(),
            method='MAX'
        )


if __name__ == '__main__':
    segment = Segment(bicycle_facility_width=6,
                      lanes_per_direction=1,
                      parking_lane_width=1,
                      aadt=500,
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
    bike_paths = BikePath()
    print(segment.blts_score(approaches, bike_paths))
