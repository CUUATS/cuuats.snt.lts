# base classs of LTS
import pandas as pd
import numpy as np


class Lts:
    # def __init__(self):
    #     self.overall_score = 0
    #     self.segment_score = 0

    @staticmethod
    def calculate_score(score, crits):
        # if not isinstance(score, pd.DataFrame) or not isinstance(score, pd.Series):
        #     raise TypeError('df argument must be a pandas DataFrame of Series object')
        # assert len(crits) == 2
        for crit in crits:
            score.index = crit[1]
            score = score.loc[crit[0]]
        assert isinstance(score, np.int64)
        return score

    @staticmethod
    def _aggregate_score(*scores, **kwargs):
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
        return

    @staticmethod
    def _calculate_total_lanes_crossed():
        self.total_lanes_crossed = 0
        if self.segment.marked_center_lane == "No" and \
                self.approach.lane_configuration is None:
            lanes = 1
        elif self.segment.marked_center_lane == "Yes" and \
                self.approach.lane_configuration is None:
            lanes = 2
        elif self.approach.lane_configuration is None:
            lanes = 2
        else:
            lanes = len(self.approach.lane_configuration)

        self.total_lanes_crossed = lanes
        return(lanes)
