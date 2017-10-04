# blts_cuuats.py

from cuuats.datamodel import feature_class_factory as factory, MethodField
from cuuats.datamodel import D
from config import SDE_DB, APPROACH_NAME
import os


APPROACH_PATH = os.path.join(SDE_DB, APPROACH_NAME)
Approach = factory(APPROACH_PATH, follow_relationships=True)
Segment = Approach.related_classes['PCD.PCDQC.StreetSegment']
Intersection = Approach.related_classes['PCD.PCDQC.StreetIntersection']


def calculate_bikeLanewithAdjParking(self):
    score = 99
    if self.BicycleFacilityWidth is not None and self.ParkingLaneWidth is not \
            None:
        if self.LanesPerDirection is 1:
            score = calculate_score(self,
                            [[1,2,3],
                            [1,2,3],
                            [2,3,3],
                            [2,4,4]],

                            ['self.IDOTAADT <= 1000 or self.IDOTAADT is None',
                             'self.IDOTAADT <= 3000',
                             'self.IDOTAADT <= 30000',
                             'True'],

                            ['self.BicycleFacilityWidth + self.ParkingLaneWidth >= 15',
                             'self.BicycleFacilityWidth + self.ParkingLaneWidth > 13',
                             'True'])
        else:
            score = calculate_score(self,
                                    [[2,3],
                                    [2,3],
                                    [3,3],
                                    [3,4]],

                                    ['self.IDOTAADT <= 1000 or self.IDOTAADT is None',
                                     'self.IDOTAADT <= 3000',
                                     'self.IDOTAADT <= 30000',
                                     'True'],

                                    ['self.BicycleFacilityWidth + '
                                     'self.ParkingLaneWidth >= 15',
                                     'True'])

    self.bikeLaneWithAdjPkScore = score
    return(score)


def calculate_bikeLanewithoutAdjParking(self):
    score = 99
    if self.BicycleFacilityWidth is not None:
        if self.LanesPerDirection is 1:
            score = calculate_score(self,
                                    [[1,1,2],
                                    [2,3,3],
                                    [3,4,4]],

                                    ['self.IDOTAADT <= 3000 or self.IDOTAADT is None',
                                     'self.IDOTAADT <= 30000',
                                     'True'],

                                    ['self.BicycleFacilityWidth >= 7',
                                     'self.BicycleFacilityWidth >= 5.5',
                                     'True'])
        else:
            score = calculate_score(self,
                                    [[1, 3],
                                     [2, 3],
                                     [3, 4]],

                                    ['self.IDOTAADT <= 3000 or self.IDOTAADT is None',
                                     'self.IDOTAADT <= 30000',
                                     'True'],

                                    ['self.BicycleFacilityWidth >= 7',
                                     'True'])

    self.bikeLaneWithoutAdjPkScore = score
    return(score)


def calculate_mixTraffic(self):
    score = 0
    score = calculate_score(self,
                            [[1,2,3,4],
                            [2,3,4,4],
                            [3,4,4,4]],

                            ['self.IDOTAADT <= 1000',
                             'self.IDOTAADT <= 3000',
                             'True'],

                            ['self.LanesPerDirection in (0, None)',
                             'self.LanesPerDirection == 1',
                             'self.LanesPerDirection == 2',
                             'self.LanesPerDirection >= 3'])

    self.mixTrafficScore = score
    return(score)


def aggregate_score(*scores, **kwargs):
    score_list = [score for score in scores if score is not None]
    method = kwargs.get("method")
    score = 0

    if method == "MIN":
        score = min(score_list)
    elif method == "MAX":
        score = max(score_list)

    return(score)


def calculate_rightTurnLane(self):
    score = 0
    streetintersectionapproach = "pcd.pcdqc.streetintersectionapproach_set"

    for approach in getattr(self, streetintersectionapproach):
        if approach.LaneConfiguration is None:
            continue
        if "R" in approach.LaneConfiguration or \
            "Q" in approach.LaneConfiguration:

            new_score = calculate_score(approach,
                                    [2,3,3,4],
                                    ['"R" in self.LaneConfiguration and \
                                    self.RightTurnLength <= 150 and \
                                    self.BikeApproachAlignment is "Straight"',

                                     '"R" in self.LaneConfiguration and \
                                    self.RightTurnLength > 150 and \
                                    self.BikeApproachAlignment is "Straight"',

                                    '"R" in self.LaneConfiguration and \
                                    self.BikeApproachAlignment is "Left"',

                                     'True'])
            if score < new_score:
                score = new_score

    self.rightTurnLaneScore = score
    return(score)


def calculate_leftTurnLane(self):
    pass



def calculate_score(self, scores, *condition_sets):
    score = scores
    #assert len(score) == len(condition_sets)
    for condition_set in condition_sets:
        for index, condition in enumerate(condition_set):
            if (eval(condition)):
                score = score[index]
                break
        # Loop through an enumeration of the conditions in this set, evaluating
        # each one. When a condition evalutes to True:
        # - Set score = score[i], where i is the index of the condition
        # - Break out of the inner loop.
    #
    # assert isinstance(score, Number)
    return(score)






def calculate_BLTS(self, field_name):
    self._calculate_MixTraffic()
    self._calculate_BikeLaneWithoutAdjParking()
    self._calculate_BikeLaneWithAdjParking()
    self.segmentScore = self._aggregate_Score(self.bikeLaneWithAdjPkScore,
                         self.bikeLaneWithoutAdjPkScore,
                         self.mixTrafficScore,
                         method="MIN")
    self._calculate_RightTurnLane()






Segment._calculate_BLTS = calculate_BLTS
Segment._calculate_MixTraffic = calculate_mixTraffic
Segment._calculate_BikeLaneWithoutAdjParking = calculate_bikeLanewithoutAdjParking
Segment._calculate_BikeLaneWithAdjParking = calculate_bikeLanewithAdjParking
Segment._aggregate_Score = aggregate_score
Segment._calculate_RightTurnLane = calculate_rightTurnLane
Segment._calculate_LeftTurnLane = calculate_leftTurnLane

# Override the BLTSScore field with a method field.
Segment.BLTS_test = MethodField(
    'BLTS Score',
    method_name='_calculate_BLTS'
)

# Registered call
Approach.register(APPROACH_PATH)

for segment in Segment.objects.filter(InUrbanizedArea=D('Yes')):
    segment.BLTS_test
    #segment.save()

