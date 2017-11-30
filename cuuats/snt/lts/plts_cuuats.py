# plts_cuuats.py
# This scripts uses the cuuats datamodel to calculate the PLTS scores

from cuuats.datamodel import feature_class_factory as factory, MethodField
from cuuats.datamodel import D
from cuuats.datamodel.manytomany import ManyToManyField
from config import SDE_DB, SEGMENT_NAME, SIDEWALK_NAME, REL_NAME, LANDUSE_DICT
import os


SEGMENT_PATH = os.path.join(SDE_DB, SEGMENT_NAME)
SIDEWALK_PATH = os.path.join(SDE_DB, SIDEWALK_NAME)
Segment = factory(SEGMENT_PATH)
Sidewalk = factory(SIDEWALK_PATH)


# Create a many-to-many field for the Segment
def calculate_sidewalk_conditions(self):
    score = 0
    score = calculate_score(
        self,
        [[4, 4, 4, 4],
         [3, 3, 3, 4],
         [2, 2, 3, 4],
         [1, 1, 2, 3]],
        ['self.sidewalk_width < 4',
         'self.sidewalk_width < 5',
         'self.sidewalk_width < 6',
         'True'],
        ['self.sidewalk_cond is "Good"',
         'self.sidewalk_cond is "Fair"',
         'self.sidewalk_cond is "Poor"',
         'True']
    )

    self.sidewalk_condition_score = score
    return score


def calculate_physical_buffer(self):
    score = 0
    score = calculate_score(
        self,
        [[2, 3, 3, 4],
         [2, 2, 2, 2],
         [1, 2, 2, 2],
         [1, 1, 1, 2]],
        ['self.buffer_type == "No Buffer"',
         'self.buffer_type == "Solid Buffer"',
         'self.buffer_type == "Landscaped"',
         'True'],
         # 'self.buffer_type is "Landscaped With Trees"'],
        ['self.PostedSpeed <= 25',
         'self.PostedSpeed == 30',
         'self.PostedSpeed == 35',
         'True']
    )

    self.physical_buffer_score = score
    return score


def calculate_total_buffering_width(self):
    score = calculate_score(
        self,
        [[2, 2, 1, 1, 1],
         [3, 2, 2, 1, 1],
         [4, 3, 2, 1, 1],
         [4, 4, 3, 2, 2]],
        ['self.TotalLanes <= 2',
         'self.TotalLanes == 3',
         'self.TotalLanes <= 5',
         'True'],
        ['self.buffer_width < 5',
         'self.buffer_width < 10',
         'self.buffer_width < 15',
         'self.buffer_width < 25',
         'True']
    )

    self.total_buffering_width_score = score
    return score


def calculate_general_landuse(self):
    self.general_landuse_score = int(self.OverallLandUse)
    #self.general_landuse_score = LANDUSE_DICT.get(self.general_landuse, 0)
    return self.general_landuse_score


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


def convert_score(self, score):
    if score > 80:
        score = 'Good'
    elif score > 70:
        score = 'Fair'
    elif score > 60:
        score = 'Poor'
    else:
        score = 'Very Poor'
    return score


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


def convert_feet_to_inches(self, feet):
    if feet is None:
        return 0
    else:
        return float(feet) / 12


def categorize_functional_class(self, category):
    if category is None:
        return "C"
    if category >= 4:
        return "C"
    else:
        return "A"


def calculate_total_lanes_crossed(self, lane_conf):
    if self.MarkedCenterLine == "No" and lane_conf is None:
        return 1
    elif self.MarkedCenterLine == "Yes" and lane_conf is None:
        return 2
    elif lane_conf is None:
        return 2
    else:
        return len(lane_conf)


def calculate_unsignalized_collector_crossing_score(self):
    score = 0
    score = calculate_score(
        self,
        [[1, 1],
         [1, 2],
         [2, 2],
         [3, 3]],
        ['self.PostedSpeed <= 25',
         'self.PostedSpeed == 30',
         'self.PostedSpeed == 35',
         'True'],
        ['self.lanecrossed <= 1',
         'True']
    )
    return score


def calculate_unsignalized_arterial_crossing_score(self):
    score = 0
    if self.lanecrossed <= 2:
        score = calculate_score(
            self,
            [[2, 2, 3],
             [2, 3, 3],
             [3, 3, 4],
             [3, 4, 4]],
            ['self.PostedSpeed <= 25',
             'self.PostedSpeed == 30',
             'self.PostedSpeed == 35',
             'True'],
            ['self.IDOTAADT < 5000',
             'self.IDOTAADT < 9000',
             'True']
        )
    else:
        score = calculate_score(
            self,
            [[3, 3, 4],
             [3, 3, 4],
             [3, 4, 4],
             [4, 4, 4]],
            ['self.PostedSpeed <= 25',
             'self.PostedSpeed == 30',
             'self.PostedSpeed == 35',
             'True'],
            ['self.IDOTAADT < 8000',
             'self.IDOTAADT < 12000',
             'True']
        )
    return score


def calculate_crossing_score(self):
    if self._categorize_functional_class(self.FunctionalClassification) == "A":
        temp_score = self._calculate_unsignalized_arterial_crossing_score()
        if temp_score > self.unsignalized_arterial_crossing_score:
            self.unsignalized_arterial_crossing_score = temp_score
    else:
        temp_score = self._calculate_unsignalized_collector_crossing_score()
        if temp_score > self.unsignalized_collector_crossing_score:
            self.unsignalized_collector_crossing_score = temp_score


def calculate_plts(self, field_name):
    self.sidewalk_score = 4

    # find score with approach attributes
    self.unsignalized_arterial_crossing_score = 0
    self.unsignalized_collector_crossing_score = 0
    self.streetintersectionapproach = "pcd.pcdqc.streetintersectionapproach_set"
    for approach in getattr(self, self.streetintersectionapproach):
        # grabbing the attributes from approach
        self.LaneConfiguration = approach.LaneConfiguration
        self.lanecrossed = self._calculate_total_lane_crossed(
            self.LaneConfiguration)
        # do calculation
        self._calculate_crossing_score()

    # find score with sidewalk attributes
    for sidewalk in getattr(self, 'sidewalks'):
        self.sidewalk_cond = self._convert_score(sidewalk.ScoreCompliance)
        self.sidewalk_width = self._convert_feet_to_inches(sidewalk.Width)
        self.buffer_type = sidewalk.BufferType
        self.buffer_width = sidewalk.BufferWidth


        self._calculate_sidewalk_condition()
        self._calculate_physical_buffer()
        self._calculate_total_buffering_width()
        self._calculate_general_laneuse()

        self.sidewalk_overall_score = self._aggregate_score(
            self.sidewalk_condition_score,
            self.physical_buffer_score,
            self.total_buffering_width_score,
            self.general_landuse_score,
            self.unsignalized_arterial_crossing_score,
            self.unsignalized_collector_crossing_score,
            method="MAX"
        )

        if self.sidewalk_score > self.sidewalk_overall_score:
            self.sidewalk_score = self.sidewalk_overall_score

    print(self.sidewalk_score)
    return self.sidewalk_score

Segment._calculate_plts = calculate_plts
Segment._calculate_sidewalk_condition = calculate_sidewalk_conditions
Segment._calculate_physical_buffer = calculate_physical_buffer
Segment._calculate_total_buffering_width = calculate_total_buffering_width
Segment._calculate_general_laneuse = calculate_general_landuse
Segment._aggregate_score = aggregate_score
Segment._convert_score = convert_score
Segment._convert_feet_to_inches = convert_feet_to_inches
Segment._categorize_functional_class = categorize_functional_class
Segment._calculate_crossing_score = calculate_crossing_score
Segment._calculate_unsignalized_collector_crossing_score = \
    calculate_unsignalized_collector_crossing_score
Segment._calculate_unsignalized_arterial_crossing_score = \
    calculate_unsignalized_arterial_crossing_score
Segment._calculate_total_lane_crossed = calculate_total_lanes_crossed

Segment.sidewalks = ManyToManyField(
    "Sidewalks",
    related_class=Sidewalk,
    relationship_class=REL_NAME,
    foreign_key="StreetSegmentID",
    related_foreign_key="SidewalkSegmentID",
    primary_key="SegmentID",
    related_primary_key="SegmentID"
)

# Override the BLTSScore field with a method field.
Segment.PLTSScore = MethodField(
    'PLTS Score',
    method_name='_calculate_plts'
)

# Registered call
Segment.register(SEGMENT_PATH)
Sidewalk.register(SIDEWALK_PATH)

if __name__ == "__main__":
    with Segment.workspace.edit():
        for segment in Segment.objects.filter(InUrbanizedArea=D('Yes')):
            segment.PLTSScore
            segment.save()
