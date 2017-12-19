# alts_cuuats.py
# This script uses cuuats datamodel to calculate the Automobile Level of
# Traffic Stress scores

from cuuats.datamodel import feature_class_factory as factory, MethodField
from cuuats.datamodel import D
from cuuats.datamodel.manytomany import ManyToManyField
from config import SDE_DB, SEGMENT_NAME, APPROACH_NAME, INTERSECTION_NAME
import os

APPROACH_PATH = os.path.join(SDE_DB, APPROACH_NAME)
Approach = factory(APPROACH_PATH, follow_relationships=True)
Segment = Approach.related_classes[SEGMENT_NAME]
Intersection = Approach.related_classes[INTERSECTION_NAME]


def aggregate_score(self, *scores, **kwargs):
    """
    this function aggregate number of scores based on *scores
    :param self: self
    :param scores: scores arguments
    :param kwargs: "MAX" - returns maximum, "MIN" - return minimum
    :return: int score
    """
    score_list = [score for score in scores if score is not None]
    method = kwargs.get("method", "MAX")
    score = 0

    if method == "MIN":
        score = min(score_list)
    elif method == "MAX":
        score = max(score_list)
    return score


def calculate_functional_class(self):
    """
    calculate the stress score based on functional classification
    :param self: 
    :return: 
    """
    pass


def calculate_bicycle_facility(self):
    """
    calculate the stress score based on present on bicycle facility on the 
    road way
    :param self: 
    :return: 
    """
    self.bicycle_facility_score = 0
    score = calculate_score(
        self,
        [1, 2, 3, 4],
        ['self.BicycleFacilityType is None',
         'self.BicycleFacilityType == "Buffered Bike Lanes"',
         'self.BicycleFacilityType == "Standard Bike Lanes" or '
         'self.BicycleFacilityType == "Bike Route"',
         'True']
    )

    self.bicycle_facility_score = score
    return self.bicycle_facility_score


def calculate_score(self, scores, *condition_sets):
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


def calculate_alts(self, field_name):
    self._calculate_bicycle_facility()
    self.overallScore = self._aggregate_score(
        self.bicycle_facility_score,
        method="MAX"
    )

    print(self.overallScore)
    return self.overallScore


Segment._aggregate_score = aggregate_score
Segment._calculate_alts = calculate_alts
Segment._calculate_bicycle_facility = calculate_bicycle_facility

Segment.ALTSScore = MethodField(
    'ALTS Score',
    method_name='_calculate_alts'
)


if __name__ == "__main__":
    with Segment.workspace.edit():
        for segment in Segment.objects.filter(InUrbanizedArea=D('Yes')):
            segment.ALTSScore
            segment.save()
            