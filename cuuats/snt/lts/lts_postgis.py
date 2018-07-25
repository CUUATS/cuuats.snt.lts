## base classs of LTS

class Lts:
    def __init__(self):
        self.overall_score = 0
        self.segment_score = 0

    def _calculate_score(self, scores, *condition_sets):
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

    def _get_high_score(self, *scores):
        return 
