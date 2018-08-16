# base classs of LTS


class Lts:
    # def __init__(self):
    #     self.overall_score = 0
    #     self.segment_score = 0

    @staticmethod
    def _calculate_score(scores, *condition_sets):
        """
        this function takes the scores and condition_sets and return the score
        based on which argument is true
        :param self: self
        :param scores: list of scores
        :param condition_sets: lists of conditions
        :return: int score
        """
        score = scores
        for condition_set in condition_sets:
            assert len(score) == len(condition_set)
            for index, condition in enumerate(condition_set):
                if eval(condition):
                    score = score[index]
                    break
        assert isinstance(score, int)
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
