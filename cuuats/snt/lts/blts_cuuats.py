# blts_cuuats.py
# This scripts uses the cuuats datamodel to calculate the BLTS scores

from cuuats.datamodel import feature_class_factory as factory, MethodField
from cuuats.datamodel import D
from config import SDE_DB, APPROACH_NAME
import os

APPROACH_PATH = os.path.join(SDE_DB, APPROACH_NAME)
Approach = factory(APPROACH_PATH, follow_relationships=True)
Segment = Approach.related_classes['PCD.PCDQC.StreetSegment']
Intersection = Approach.related_classes['PCD.PCDQC.StreetIntersection']


def calculate_bikelane_with_adj_parking(self):
    """
    This function calculates the score of bike lane with adjacent parking
    spaces scores based on the criteria
    :param self: self
    :return: int score
    """
    score = 99
    if self.BicycleFacilityWidth is not None and self.ParkingLaneWidth is not \
            None:
        if self.LanesPerDirection is 1 or self.LanesPerDirection is None:
            score = calculate_score(
                self,
                [[1, 2, 3],
                 [1, 2, 3],
                 [2, 3, 3],
                 [2, 4, 4]],
                ['self.IDOTAADT <= 1000 or self.IDOTAADT is None',
                 'self.IDOTAADT <= 3000',
                 'self.IDOTAADT <= 30000',
                 'True'],
                ['self.BicycleFacilityWidth + self.ParkingLaneWidth >= 15',
                 'self.BicycleFacilityWidth + self.ParkingLaneWidth > 13',
                 'True'])
        else:
            score = calculate_score(
                self,
                [[2, 3],
                 [2, 3],
                 [3, 3],
                 [3, 4]],

                ['self.IDOTAADT <= 1000 or self.IDOTAADT is None',
                 'self.IDOTAADT <= 3000',
                 'self.IDOTAADT <= 30000',
                 'True'],

                ['self.BicycleFacilityWidth + '
                 'self.ParkingLaneWidth >= 15',
                 'True'])

    self.bikeLaneWithAdjPkScore = score
    return score


def calculate_bikelane_without_adj_parking(self):
    """
    This functions calculates the score of bike lanes without adjacent
    parking based on the specified criteria
    :param self: self
    :return: int score
    """
    score = 99
    if self.BicycleFacilityWidth is not None:
        if self.LanesPerDirection is 1 or self.LanesPerDirection is None:
            score = calculate_score(
                self,
                [[1, 1, 2],
                 [2, 3, 3],
                 [3, 4, 4]],
                ['self.IDOTAADT <= 3000 or self.IDOTAADT is None',
                 'self.IDOTAADT <= 30000',
                 'True'],
                ['self.BicycleFacilityWidth >= 7',
                 'self.BicycleFacilityWidth >= 5.5',
                 'True'])
        else:
            score = calculate_score(
                self,
                [[1, 3],
                 [2, 3],
                 [3, 4]],
                ['self.IDOTAADT <= 3000 or self.IDOTAADT is None',
                 'self.IDOTAADT <= 30000',
                 'True'],
                ['self.BicycleFacilityWidth >= 7',
                 'True'])

    self.bikeLaneWithoutAdjPkScore = score
    return score


def calculate_mix_traffic(self):
    """
    this function calculate the mix traffic scores based on the specify
    criterias
    :param self: self
    :return: int score
    """
    score = 0
    score = calculate_score(
        self,
        [[1, 2, 3, 4],
         [2, 3, 4, 4],
         [3, 4, 4, 4]],
        ['self.IDOTAADT <= 1000',
         'self.IDOTAADT <= 3000',
         'True'],
        ['self.LanesPerDirection in (0, None)',
         'self.LanesPerDirection == 1',
         'self.LanesPerDirection == 2',
         'self.LanesPerDirection >= 3'])

    self.mixTrafficScore = score
    return score


def calculate_right_turn_lane(self):
    """
    this function calculates the right turn lane scores based on the criterias
    :param self: self
    :return: int score
    """
    if self.LaneConfiguration is None:
        return
    if "R" in self.LaneConfiguration or \
       "Q" in self.LaneConfiguration:

        new_score = calculate_score(
            self,
            [2, 3, 3, 4],
            ['"R" in self.LaneConfiguration and \
             self.RightTurnLength <= 150 and \
             self.BikeApproachAlignment is "Straight"',

             '"R" in self.LaneConfiguration and \
             self.RightTurnLength > 150 and \
             self.BikeApproachAlignment is "Straight"',

             '"R" in self.LaneConfiguration and \
             self.BikeApproachAlignment is "Left"',

             'True'])

        if self.rightTurnLaneScore < new_score:
            self.rightTurnLaneScore = new_score

    return self.rightTurnLaneScore


def calculate_left_turn_lane(self):
    """
    this function calculate the left turn lane score based on the criterias
    :param self: self
    :return: int score
    """

    if self.LaneConfiguration is None:
        return
    if "K" in self.LaneConfiguration or \
       "L" in self.LaneConfiguration:
        new_score = calculate_score(
            self,
            [4, 4, 4],
            ['self.PostedSpeed <= 25',
             'self.PostedSpeed == 30',
             'self.PostedSpeed >= 35'])
        if self.leftTurnLaneScore < new_score:
            self.leftTurnLaneScore = new_score
    else:
        self.lanecrossed = self._calculate_Lanecrossed(
            self.LaneConfiguration)
        new_score = calculate_score(
            self,
            [[2, 2, 3],
             [2, 3, 4],
             [3, 4, 4]],

            ['self.PostedSpeed <= 25',
             'self.PostedSpeed == 30',
             'self.PostedSpeed >= 35'],

            ['self.lanecrossed == 0',
             'self.lanecrossed == 1',
             'self.lanecrossed >= 2'])

        if self.leftTurnLaneScore < new_score:
            self.leftTurnLaneScore = new_score

    return self.leftTurnLaneScore


def calculate_unsignalized_crossing_without_median(self):
    """
    this function calculates the unsignalized crossing without median based
    on the criterias
    :param self: self
    :return: int score
    """
    if self.LaneConfiguration is None:
        return
    self.totalLanes = len(self.LaneConfiguration)
    new_score = calculate_score(
        self,
        [[1, 2, 4],
         [1, 2, 4],
         [2, 3, 4],
         [3, 4, 4]],

        ['self.PostedSpeed <= 25',
         'self.PostedSpeed == 30',
         'self.PostedSpeed == 35',
         'True'],

        ['self.totalLanes <= 3',
         'self.totalLanes <= 5',
         'True'])

    if self.unsignalizedCrossingWithoutMedianScore < new_score:
        self.unsignalizedCrossingWithoutMedianScore = new_score

    self.unsignalizedCrossingWithoutMedianScore = new_score
    return self.unsignalizedCrossingWithoutMedianScore


def calculate_unsignalized_crossing_with_median(self):
    """
    this functions calculates the unsignalized crossing with median based on
    the criteria
    :param self: self
    :return: int score
    """
    if self.LaneConfiguration is None:
        return
    self.maxLane = self._calculate_MaxLane(self.LaneConfiguration)

    new_score = calculate_score(
        self,
        [[1, 1, 2],
         [1, 2, 3],
         [2, 3, 4],
         [3, 4, 4]],

        ['self.PostedSpeed <= 25',
         'self.PostedSpeed == 30',
         'self.PostedSpeed == 35',
         'True'],

        ['self.maxLane <= 2',
         'self.maxLane == 3',
         'True'])
    if self.unsignalizedCrossingWithMedianScore < new_score:
        self.unsignalizedCrossingWithMedianScore = new_score

    self.unsignalizedCrossingWithMedianScore = new_score
    return self.unsignalizedCrossingWithMedianScore


def calculate_max_lane(self, lane_config):
    """
    this function takes lane configuration string and return the max lane in
    either direction
    :param self: self
    :param lane_config: coded string of lane configuration
    :return: int represent max lane
    """
    if lane_config is None:
        max_lane = 1
    else:
        away_lane = len(lane_config[lane_config.find("X"):
                        lane_config.rfind("X")+1])
        incomeing_lane = len(lane_config[lane_config.rfind("X")+1:])
        max_lane = max(away_lane, incomeing_lane)

    return max_lane


def calculate_lanecrossed(self, lane_config):
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


def aggregate_score(self, *scores, **kwargs):
    """
    this function aggregate number of scores based on *scores
    :param self: self
    :param scores: scores arguments
    :param kwargs: "MAX" - returns maximum, "MIN" - return minimum
    :return: int score
    """
    score_list = [score for score in scores if score is not None]
    method = kwargs.get("method")
    score = 0

    if method == "MIN":
        score = min(score_list)
    elif method == "MAX":
        score = max(score_list)
    return score


def calculate_blts(self, field_name):
    """
    this is a method field function that calculated the score for the
    BLTSScore field
    :param self: self
    :param field_name: required argument
    :return: blts score
    """
    # Segment condition scores
    self._calculate_mix_traffic()
    self._calculate_bikelane_without_adj_parking()
    self._calculate_bikelane_with_adj_parking()
    self.segmentScore = self._aggregate_Score(
                self.bikeLaneWithAdjPkScore,
                self.bikeLaneWithoutAdjPkScore,
                self.mixTrafficScore,
                method="MIN")

    # Loop through score required approaches
    self.streetintersectionapproach = "pcd.pcdqc.streetintersectionapproach_set"
    self.rightTurnLaneScore = 0
    self.leftTurnLaneScore = 0
    self.unsignalizedCrossingWithoutMedianScore = 0
    self.unsignalizedCrossingWithMedianScore = 0
    for approach in getattr(self, self.streetintersectionapproach):
        self.LaneConfiguration = approach.LaneConfiguration
        self.RightTurnLength = approach.RightTurnLength
        self.BikeApproachAlignment = approach.BikeApproachAlignment
        self._calculate_right_turn_lane()
        self._calculate_left_turn_lane()
        self._calculate_unsignalized_crossing_without_median()
        self._calculate_unsignalized_crossing_with_median()

    self.overallScore = self._aggregate_Score(
                self.segmentScore,
                self.rightTurnLaneScore,
                self.leftTurnLaneScore,
                self.unsignalizedCrossingWithoutMedianScore,
                self.unsignalizedCrossingWithMedianScore,
                method="MAX")

    print(self.overallScore)
    return self.overallScore


# Adding functions as methods for the Segment Class
Segment._calculate_blts = calculate_blts
Segment._calculate_mix_traffic = calculate_mix_traffic
Segment._calculate_bikelane_without_adj_parking = \
    calculate_bikelane_without_adj_parking
Segment._calculate_bikelane_with_adj_parking = \
    calculate_bikelane_with_adj_parking
Segment._aggregate_Score = aggregate_score
Segment._calculate_right_turn_lane = calculate_right_turn_lane
Segment._calculate_left_turn_lane = calculate_left_turn_lane
Segment._calculate_Lanecrossed = calculate_lanecrossed
Segment._calculate_unsignalized_crossing_without_median = \
    calculate_unsignalized_crossing_without_median
Segment._calculate_unsignalized_crossing_with_median = \
    calculate_unsignalized_crossing_with_median
Segment._calculate_MaxLane = calculate_max_lane


# Override the BLTSScore field with a method field.
Segment.BLTSScore = MethodField(
    'BLTS Score',
    method_name='_calculate_blts'
)

# Registered call
Approach.register(APPROACH_PATH)

if __name__ == "__main__":
    for segment in Segment.objects.filter(InUrbanizedArea=D(
            'Yes')):
        segment.BLTSScore
        # segment.save()
