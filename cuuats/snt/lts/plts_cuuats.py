# plts_cuuats.py
# This scripts uses the cuuats datamodel to calculate the PLTS scores

from cuuats.datamodel import feature_class_factory as factory, MethodField
from cuuats.datamodel import D
from config import SDE_DB, SEGMENT_NAME, SIDEWALK_NAME, REL_NAME
import os


SEGMENT_PATH = os.path.join(SDE_DB, SEGMENT_NAME)
SIDEWALK_PATH = os.path.join(SDE_DB, SIDEWALK_NAME)
Segment = factory(SEGMENT_PATH, follow_relationships=False)
Sidewalk = factory(SIDEWALK_PATH, follow_relationships=False)

# Create a many-to-many field for the Segment


def calculate_sidewalk_conditions(self):
    score = 0
    for sw in Segment.Sidewalks:
        # Calculate sidewalk condition
    return score


def calculate_plts(self, field_name):
    score = calculate_sidewalk_conditions(self)
    return score


Segment._calculate_blts = calculate_plts
Segment._calculate_sidewalk_condition = calculate_sidewalk_conditions

Segment.Sidewalks = ManyToManyField(
    "Sidewalks",
    related_class = Sidewalk,
    relationship_class = REL_NAME,
    foreign_key = "StreetSegmentID",
    related_foreign_key = "SidewalkSegmentID",
    primary_key = "SegmentID",
    related_primary_key = "SidewalkID"
)


# Override the BLTSScore field with a method field.
Segment.PLTSScore = MethodField(
    'PLTS Score',
    method_name='_calculate_plts'
)

# Registered call
Segment.register(SEGMENT_PATH)

if __name__ == "__main__":
    for segment in Segment.objects.filter(InUrbanizedArea=D('Yes')):
        segment.PLTSScore
        # segment.save()