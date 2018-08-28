# base classs of LTS
import pandas as pd
import numpy as np


class Lts:
    # def __init__(self):
    #     self.overall_score = 0
    #     self.segment_score = 0

    @staticmethod
    def remove_none(value):
        if value is None:
            value = 0
        return value

    @staticmethod
    def calculate_score(score, crits):
        if (not isinstance(score, pd.DataFrame)) and \
           (not isinstance(score, pd.Series)):
            raise TypeError(
                'df argument must be a pandas DataFrame of Series object')

        if isinstance(score, pd.DataFrame):
            assert len(crits) == 2
        elif isinstance(score, pd.Series):
            assert len(crits) == 1

        for crit in crits:
            score.index = crit[1]
            score = score.loc[crit[0]]
        assert isinstance(score, np.int64)
        return score

    @staticmethod
    def aggregate_score(*scores, **kwargs):
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

    @staticmethod
    def _get_high_score(*scores):
        pass

    @staticmethod
    def calculate_ltl_crossed(lane_config):
        """
        this function takes lane configuration string and return the lanecrossed
        from righter most lane to the left turn lane
        :param self: self
        :param lane_config: coded string of lane_config
        :return:
        """
        if lane_config is None:
            lanecrossed = 0
        elif lane_config == "X" or lane_config == "XX" or lane_config == "XXX":
            lanecrossed = 0
        else:
            lanecrossed = len(lane_config) - \
                          lane_config.rfind("X") - 2
        return lanecrossed

    @staticmethod
    def calculate_total_lanes_crossed(marked_center_lane, lane_config):
        total_lanes_crossed = 0
        if marked_center_lane == "No" and lane_config is None:
            total_lanes_crossed = 1
        elif marked_center_lane == "Yes" and lane_config is None:
            total_lanes_crossed = 2
        elif lane_config is None:
            total_lanes_crossed = 2
        else:
            total_lanes_crossed = len(lane_config)

        return total_lanes_crossed
