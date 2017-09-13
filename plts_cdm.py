# plts_cdm.py
# Purpose: This script follows the Pedestrian Level of Traffic Stress
# assessment and assign score to each sidewalk segment.

from cuuats.datamodel import feature_class_factory as factory, MethodField
import arcpy
from config import SW_COND_TABLE, BUFFER_WIDTH_TABLE, BUFFER_TYPE_TABLE, \
    LANDUSE_DICT
import os

SDE_DB = r"G:\Resources\Connections\PCD_Edit_aadt.sde"
SIDEWALK_NAME = "PCD.PCDQC.Roadway\PCD.PCDQC.StreetSegment"
SDE_PATH = os.path.join(SDE_DB, SIDEWALK_NAME)

Sidewalk = factory(SDE_PATH)
Segment = factory(SDE_PATH)


import pdb; pdb.set_trace()


def calculate_sidewalkCondition(self, fieldname):
    score = 0
    if self.Width < 4:
        if self.SidewalkCondition == "Good":
            score = SW_COND_TABLE[0][0]
        elif self.SidewalkCondition == "Fair":
            score = SW_COND_TABLE[0][1]
        elif self.SidewalkCondition == "Poor":
            score = SW_COND_TABLE[0][2]
        else:
            score = SW_COND_TABLE[0][3]
    elif self.Width < 5:
        if self.SidewalkCondition == "Good":
            score = SW_COND_TABLE[1][0]
        elif self.SidewalkCondition == "Fair":
            score = SW_COND_TABLE[1][1]
        elif self.SidewalkCondition == "Poor":
            score = SW_COND_TABLE[1][2]
        else:
            score = SW_COND_TABLE[1][3]
    elif self.Width < 6:
        if self.SidewalkCondition == "Good":
            score = SW_COND_TABLE[2][0]
        elif self.SidewalkCondition == "Fair":
            score = SW_COND_TABLE[2][1]
        elif self.SidewalkCondition == "Poor":
            score = SW_COND_TABLE[2][2]
        else:
            score = SW_COND_TABLE[2][3]
    else:
        if self.SidewalkCondition == "Good":
            score = SW_COND_TABLE[3][0]
        elif self.SidewalkCondition == "Fair":
            score = SW_COND_TABLE[3][1]
        elif self.SidewalkCondition == "Poor":
            score = SW_COND_TABLE[3][2]
        else:
            score = SW_COND_TABLE[3][3]

    return(score)



def calculate_bufferType(self, fieldname):
    score = 0
    if self.bufferType == "No Buffer":
        if self.Speed <= 25:
            score = BUFFER_TYPE_TABLE[0][0]
        elif self.Speed  == 30:
            score = BUFFER_TYPE_TABLE[0][1]
        elif self.Speed == 35:
            score = BUFFER_TYPE_TABLE[0][2]
        else:
            score = BUFFER_TYPE_TABLE[0][3]
    elif self.bufferType == "Solid Surface":
        if self.Speed <= 25:
            score = BUFFER_TYPE_TABLE[1][0]
        elif self.Speed == 30:
            score = BUFFER_TYPE_TABLE[1][1]
        elif self.Speed == 35:
            score = BUFFER_TYPE_TABLE[1][2]
        else:
            score = BUFFER_TYPE_TABLE[1][3]
    elif self.bufferType == "Landscaped":
        if self.Speed <= 25:
            score = BUFFER_TYPE_TABLE[2][0]
        elif self.Speed == 30:
            score = BUFFER_TYPE_TABLE[2][1]
        elif self.Speed == 35:
            score = BUFFER_TYPE_TABLE[2][2]
        else:
            score = BUFFER_TYPE_TABLE[2][3]
    elif self.bufferType == "Landscaped with trees" or self.bufferType == \
            "Vertical":
        if self.Speed <= 25:
            score = BUFFER_TYPE_TABLE[3][0]
        elif self.Speed == 30:
            score = BUFFER_TYPE_TABLE[3][1]
        elif self.Speed == 35:
            score = BUFFER_TYPE_TABLE[3][2]
        else:
            score = BUFFER_TYPE_TABLE[3][3]

    return(score)



def calculate_bufferWidth(self, fieldname):
    score = 0
    if self.StreetID.TotalLane == 2:
        if self.BufferWidth < 5:
            score = BUFFER_WIDTH_TABLE[0][0]
        elif self.BufferWidth < 10:
            score = BUFFER_WIDTH_TABLE[0][1]
        elif self.BufferWidth < 15:
            score = BUFFER_WIDTH_TABLE[0][2]
        elif self.BufferWidth < 25:
            score = BUFFER_WIDTH_TABLE[0][3]
        else:
            score = BUFFER_WIDTH_TABLE[0][4]
    elif self.StreetID.TotalLane == 3:
        if self.BufferWidth < 5:
            score = BUFFER_WIDTH_TABLE[1][0]
        elif self.BufferWidth < 10:
            score = BUFFER_WIDTH_TABLE[1][1]
        elif self.BufferWidth < 15:
            score = BUFFER_WIDTH_TABLE[1][2]
        elif self.BufferWidth < 25:
            score = BUFFER_WIDTH_TABLE[1][3]
        else:
            score = BUFFER_WIDTH_TABLE[1][4]
    elif self.StreetID.TotalLane == 4 or self.StreetID.TotalLane == 5:
        if self.BufferWidth < 5:
            score = BUFFER_WIDTH_TABLE[2][0]
        elif self.BufferWidth < 10:
            score = BUFFER_WIDTH_TABLE[2][1]
        elif self.BufferWidth < 15:
            score = BUFFER_WIDTH_TABLE[2][2]
        elif self.BufferWidth < 25:
            score = BUFFER_WIDTH_TABLE[2][3]
        else:
            score = BUFFER_WIDTH_TABLE[2][4]
    elif self.StreetID.TotalLane == 6:
        if self.BufferWidth < 5:
            score = BUFFER_WIDTH_TABLE[3][0]
        elif self.BufferWidth < 10:
            score = BUFFER_WIDTH_TABLE[3][1]
        elif self.BufferWidth < 15:
            score = BUFFER_WIDTH_TABLE[3][2]
        elif self.BufferWidth < 25:
            score = BUFFER_WIDTH_TABLE[3][3]
        else:
            score = BUFFER_WIDTH_TABLE[3][4]


    return(score)



def calculate_landuse(self, fieldname):
    score = 0
    score = LANDUSE_DICT.get(self.LandUse, None)
    return(score)


def aggregate_score(*args, **kwargs):
    """
    This function takes input scores as arguments, and aggregate the scores 
    based on the method choosen.
    :param args:  scores as arguments
    :param kwargs: the method of which score are aggregated:
     'MAX' return the maximum of the input scores
     'MIN' return the minimum of the input scores
    :return: 
    """
    if kwargs.get("method") == "MAX":
        score = 0
        for i in args:
            if score < i:
                score = i
    if kwargs.get("method") == "MIN":
        score = 99
        for i in args:
            if score > i:
                score = i

    return(score)



def calculate_PLTS(self, fieldname):
    final_score = 0
    sw_cond_score = calculate_sidewalkCondition(self, fieldname)
    bufferType_score = calculate_bufferType(self, fieldname)
    bufferWidth_score = calculate_bufferWidth(self, fieldname)
    landuse_score = calculate_landuse(self, fieldname)
    final_score = aggregate_score(sw_cond_score, bufferType_score,
                                  bufferWidth_score, landuse_score,
                                  method="MAX")
    return(final_score)


# Add the calculate plts method to the Sidewalk class.
Sidewalk._calculate_PLTS = calculate_PLTS

# Override the PLTSScore field with a method field.
Sidewalk.PLTSScore = MethodField(
    'PLTS Score',
    method_name='_calculate_PLTS'
)

# Clear the field cache.
del Sidewalk._fields

# The newly-added field needs to be registered with the feature class.
layer_fields = Sidewalk.workspace.get_layer_fields(Sidewalk.name)
Sidewalk.fields['PLTSScore'].register(
    Sidewalk.workspace, Sidewalk, 'PLTSScore', Sidewalk.name, layer_fields)

if __name__ == "__main__":
    if arcpy.CheckProduct("ArcInfo") != "Available":
        print("License Not Available")
        exit()
    else:
        print("License Available")

    for segment in Segment.objects.all():
        segment.PLTSScore