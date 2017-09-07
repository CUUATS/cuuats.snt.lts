# btls_cdm.py
# Purpose: This script uses the cuuats data model package and calculate the
# Bike Level of Traffic Stress (BTLS) score for each road segment.

from cuuats.datamodel import feature_class_factory as factory, MethodField
from cuuats.datamodel import D
from config import BL_ADJ_PK_TABLE, BL_NO_ADJ_PK_TABLE, MIXED_TRAF_TABLE, \
    RTL_CRIT_TABLE, LTL_CRIT_TABLE, CROSS_NO_MED_TABLE, CROSS_HAS_MED_TABLE
import arcpy
import os


SDE_DB = r"G:\Resources\Connections\PCD_Edit_aadt.sde"
STREET_NAME = "PCD.PCDQC.StreetIntersectionApproach"
APPROACH_PATH = os.path.join(SDE_DB, STREET_NAME)


Approach = factory(APPROACH_PATH)
Intersection = Approach.related_classes['PCD.PCDQC.StreetIntersection']
Segment = Approach.related_classes['PCD.PCDQC.StreetSegment']


# method to calculate mix traffic score
def calculate_mixTraffic(self, field_name):
    """
    This function calculates the mix traffic score based on posted speed (
    need to switch to volumn later) and lanes per direction. 
    :param self: 
    :param field_name: 
    :return: int score for mix traffic with sharrow criteria
    """
    score = 0
    if self.IDOTAADT <= 1000 or self.IDOTAADT is None:
        if self.LanesPerDirection == 0:
            score = MIXED_TRAF_TABLE[0][0]
        elif self.LanesPerDirection == 1:
            score = MIXED_TRAF_TABLE[0][1]
        elif self.LanesPerDirection == 2:
            score = MIXED_TRAF_TABLE[0][2]
        else:
            score = MIXED_TRAF_TABLE[0][3]
    elif self.IDOTAADT <= 3000:
        if self.LanesPerDirection == 0:
            score = MIXED_TRAF_TABLE[1][0]
        elif self.LanesPerDirection == 1:
            score = MIXED_TRAF_TABLE[1][1]
        elif self.LanesPerDirection == 2:
            score = MIXED_TRAF_TABLE[1][2]
        else:
            score = MIXED_TRAF_TABLE[1][3]
    else:
        if self.LanesPerDirection == 0:
            score = MIXED_TRAF_TABLE[2][0]
        elif self.LanesPerDirection == 1:
            score = MIXED_TRAF_TABLE[2][1]
        elif self.LanesPerDirection == 2:
            score = MIXED_TRAF_TABLE[2][2]
        else:
            score = MIXED_TRAF_TABLE[2][3]

    # calculate sharrow
    if self.BicycleFacilityType == "Sharrows" and self.IDOTAADT <= 1000:
        if score > 1:
            score = score - 1


    return(score)



def calculate_bikeLaneWithParkingLane(self, field_name):
    """
    This function calculates the score for bike Lane with adjacent parking 
    lane, based on parking lane width, posted speed(volumn), and lanes per 
    direction.
    :param self: 
    :param field_name: 
    :return: int score for bike lane with adjacent parking lane
    """
    score = 99
    BicycleFacilityType = self.BicycleFacilityType
    #check for bicycle facility
    if BicycleFacilityType == "Standard Bike Lanes" or BicycleFacilityType ==\
            "Buffered Bike Lanes" or BicycleFacilityType == "Shared " \
                                                            "Bike/Parking " \
                                                            "Lanes":
        if self.ParkingLaneWidth is not None:
            if self.LanesPerDirection == 1 or self.LanesPerDirection == 0:
                if self.IDOTAADT <= 1000:
                    if self.BicycleFacilityWidth + self.ParkingLaneWidth >= 15:
                        score = BL_ADJ_PK_TABLE[0][0]
                    elif self.BicycleFacilityWidth + self.ParkingLaneWidth > 13:
                        score = BL_ADJ_PK_TABLE[0][1]
                    else:
                        score = BL_ADJ_PK_TABLE[0][2]
                elif self.IDOTAADT <= 3000:
                    if self.BicycleFacilityWidth + self.ParkingLaneWidth >= 15:
                        score = BL_ADJ_PK_TABLE[1][0]
                    elif self.BicycleFacilityWidth + self.ParkingLaneWidth > 13:
                        score = BL_ADJ_PK_TABLE[1][1]
                    else:
                        score = BL_ADJ_PK_TABLE[1][2]
                elif self.IDOTAADT <= 30000:
                    if self.BicycleFacilityWidth + self.ParkingLaneWidth >= 15:
                        score = BL_ADJ_PK_TABLE[2][0]
                    elif self.BicycleFacilityWidth + self.ParkingLaneWidth > 13:
                        score = BL_ADJ_PK_TABLE[2][1]
                    else:
                        score = BL_ADJ_PK_TABLE[2][2]
                else:
                    if self.BicycleFacilityWidth + self.ParkingLaneWidth >=15:
                        score = BL_ADJ_PK_TABLE[3][0]
                    elif self.BicycleFacilityWidth + self.ParkingLaneWidth > 13:
                        score = BL_ADJ_PK_TABLE[3][1]
                    else:
                        score = BL_ADJ_PK_TABLE[3][2]
            elif self.LanesPerDirection >= 2:
                if self.IDOTAADT <= 1000:
                    if self.BicycleFacilityWidth + self.ParkingLaneWidth >= 15:
                        score = BL_ADJ_PK_TABLE[0][3]
                    else:
                        score = BL_ADJ_PK_TABLE[0][4]
                elif self.IDOTAADT <= 3000:
                    if self.BicycleFacilityWidth + self.ParkingLaneWidth >= 15:
                        score = BL_ADJ_PK_TABLE[1][3]
                    else:
                        score = BL_ADJ_PK_TABLE[1][4]
                elif self.IDOTAADT <= 30000:
                    if self.BicycleFacilityWidth + self.ParkingLaneWidth >= 15:
                        score = BL_ADJ_PK_TABLE[2][3]
                    else:
                        score = BL_ADJ_PK_TABLE[2][4]
                else:
                    if self.BicycleFacilityWidth + self.ParkingLaneWidth >= 15:
                        score = BL_ADJ_PK_TABLE[3][3]
                    else:
                        score = BL_ADJ_PK_TABLE[3][4]


    return(score)



def calculate_bikeLaneWithoutParkingLane(self, field_name):
    """
    This function calculate the score for bike lane without adjacent parking 
    based on present of parking lane, lanes per direction, posted speed(
    volumn), and bike lane width. 
    :param self: 
    :param field_name: 
    :return: int score for bike lane without parking lane
    """
    score = 99
    BicycleFacilityType = self.BicycleFacilityType
    if BicycleFacilityType == "Standard Bike Lanes" or BicycleFacilityType ==\
            "Buffered Bike Lanes" or BicycleFacilityType == "Shared " \
                                                            "Bike/Parking " \
                                                            "Lanes":
        if self.ParkingLaneWidth is None:
            if self.LanesPerDirection == 1 or self.LanesPerDirection == 0:
                if self.IDOTAADT <= 3000:
                    if self.BicycleFacilityWidth >= 7:
                        score = BL_NO_ADJ_PK_TABLE[0][0]
                    elif self.BicycleFacilityWidth > 5.5:
                        score = BL_NO_ADJ_PK_TABLE[0][1]
                    else:
                        score = BL_NO_ADJ_PK_TABLE[0][2]
                elif self.IDOTAADT <= 30000:
                    if self.BicycleFacilityWidth >= 7:
                        score = BL_NO_ADJ_PK_TABLE[1][0]
                    elif self.BicycleFacilityWidth > 5.5:
                        score = BL_NO_ADJ_PK_TABLE[1][1]
                    else:
                        score = BL_NO_ADJ_PK_TABLE[1][2]
                else:
                    if self.BicycleFacilityWidth >= 7:
                        score = BL_NO_ADJ_PK_TABLE[2][0]
                    elif self.BicycleFacilityWidth > 5.5:
                        score = BL_NO_ADJ_PK_TABLE[2][1]
                    else:
                        score = BL_NO_ADJ_PK_TABLE[2][2]

            elif self.LanesPerDirection >= 2:
                if self.IDOTAADT <= 3000:
                    if self.BicycleFacilityWidth >= 7:
                        score = BL_ADJ_PK_TABLE[0][4]
                    else:
                        score = BL_ADJ_PK_TABLE[0][5]
                elif self.IDOTAADT == 30000:
                    if self.BicycleFacilityWidth >= 7:
                        score = BL_ADJ_PK_TABLE[1][4]
                    else:
                        score = BL_ADJ_PK_TABLE[1][5]
                else:
                    if self.BicycleFacilityWidth >= 7:
                        score = BL_ADJ_PK_TABLE[2][4]
                    else:
                        score = BL_ADJ_PK_TABLE[2][5]


    return(score)



def aggreage_Score(*args, **kwargs):
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



def calculate_rightTurnLane(self, field_name):
    """
    This function calculate the right turn lane score based on right turn 
    lane configuration, right turn lane length, and bike lane approach 
    alignment.  
    :param self: 
    :param field_name: 
    :return: int right turn lane score for each segment
    """
    score = 0
    streetintersectionapproach = "pcd.pcdqc.streetintersectionapproach_set"

    for approach in getattr(self, streetintersectionapproach):
        # check for any right turn lane configuration
        if approach.LaneConfiguration is None:
            continue
        if "R" in approach.LaneConfiguration or \
            "Q" in approach.LaneConfiguration:
            # check for the first row in the scoring table
            if "R" in approach.LaneConfiguration and \
                approach.RightTurnLength <= 150 and \
                approach.BikeApproachAlignment is "Straight":
                if score < RTL_CRIT_TABLE[0]:
                    score = RTL_CRIT_TABLE[0]

            elif "R" in approach.LaneConfiguration and \
                approach.RightTurnLength > 150 and \
                approach.BikeApproachAlignment is "Straight":
                if score < RTL_CRIT_TABLE[1]:
                    score = RTL_CRIT_TABLE[1]

            elif "R" in approach.LaneConfiguration and \
                approach.BikeApproachAlignment is "Left":
                if score < RTL_CRIT_TABLE[2]:
                    score = RTL_CRIT_TABLE[2]

            else:
                if score < RTL_CRIT_TABLE[3]:
                    score = RTL_CRIT_TABLE[3]

    return(score)



def _calculate_lanecrossed(laneconfiguration):
    if laneconfiguration == None:
        lanecrossed = 0
    elif laneconfiguration == "X" or \
                    laneconfiguration == "XX" or \
                    laneconfiguration == "XXX":
        lanecrossed = 0
    else:
        lanecrossed = len(laneconfiguration) - \
                      laneconfiguration.rfind("X") - 2
    return(lanecrossed)



def calculate_leftTurnLane(self, field_name):
    """
    This function calculates the left turn lane score for each segment based 
    on the left turn lane configuration, posted speed(volumn), left turn lane
    crossed.
    :param self: 
    :param field_name: 
    :return: int score for the left turn lane criteria
    """
    score = 0
    streetintersectionapproach = "pcd.pcdqc.streetintersectionapproach_set"

    for approach in getattr(self, streetintersectionapproach):
        if approach.LaneConfiguration is None:
            continue
        exclusiveLeftTurn = False
        lanecrossed = 0
        # Dual shared or exclusive left turn lane
        if "K" in approach.LaneConfiguration or \
            "L" in approach.LaneConfiguration:
            lanecrossed = _calculate_lanecrossed(approach.LaneConfiguration)
            # Speed 25 or less
            if self.PostedSpeed <= 25:
                # No lane crossed
                if lanecrossed == 0:
                    if score < LTL_CRIT_TABLE[0][3]:
                        score = LTL_CRIT_TABLE[0][3]
                # 1 lane crossed
                elif lanecrossed == 1:
                    if score < LTL_CRIT_TABLE[1][3]:
                        score = LTL_CRIT_TABLE[1][3]
                # 2+ lanes crossed
                else:
                    if score < LTL_CRIT_TABLE[2][3]:
                        score = LTL_CRIT_TABLE[2][3]
        else:
            # calculate the lane crossed
            lanecrossed = _calculate_lanecrossed(approach.LaneConfiguration)


            # Speed 25 or less
            if self.PostedSpeed <= 25:
                if lanecrossed == 0:
                    if score < LTL_CRIT_TABLE[0][0]:
                        score = LTL_CRIT_TABLE[0][0]
                elif lanecrossed == 1:
                    if score < LTL_CRIT_TABLE[0][1]:
                        score = LTL_CRIT_TABLE[0][1]
                else:
                    if score < LTL_CRIT_TABLE[0][2]:
                        score = LTL_CRIT_TABLE[0][2]
            elif self.PostedSpeed == 30:
                if lanecrossed == 0:
                    if score < LTL_CRIT_TABLE[1][0]:
                        score = LTL_CRIT_TABLE[1][0]
                elif lanecrossed == 1:
                    if score < LTL_CRIT_TABLE[1][1]:
                        score = LTL_CRIT_TABLE[1][1]
                else:
                    if score < LTL_CRIT_TABLE[1][2]:
                        score = LTL_CRIT_TABLE[1][2]
            else:
                if lanecrossed == 0:
                    if score < LTL_CRIT_TABLE[2][0]:
                        score = LTL_CRIT_TABLE[2][0]
                elif lanecrossed == 1:
                    if score < LTL_CRIT_TABLE[2][1]:
                        score = LTL_CRIT_TABLE[2][1]
                else:
                    if score < LTL_CRIT_TABLE[2][2]:
                        score = LTL_CRIT_TABLE[2][2]

    return(score)



def calculate_unsignalizedCrossingWithoutMedian(self, field_name):
    score = 0
    streetintersectionapproach = "pcd.pcdqc.streetintersectionapproach_set"
    for approach in getattr(self, streetintersectionapproach):
        if approach.LaneConfiguration is None:
            continue
        if self.PostedSpeed == 25:
            if len(approach.LaneConfiguration) <= 3 or \
                    approach.LaneConfiguration is None:
                score = CROSS_NO_MED_TABLE[0][0]
            elif len(approach.LaneConfiguration) <= 5:
                score = CROSS_NO_MED_TABLE[0][1]
            else:
                score = CROSS_NO_MED_TABLE[0][2]
        elif self.PostedSpeed == 30:
            if len(approach.LaneConfiguration) <= 3 or \
                    approach.LaneConfiguration is None:
                score = CROSS_NO_MED_TABLE[1][0]
            elif len(approach.LaneConfiguration) <= 5:
                score = CROSS_NO_MED_TABLE[1][1]
            else:
                score = CROSS_NO_MED_TABLE[1][2]
        elif self.PostedSpeed == 35:
            if len(approach.LaneConfiguration) <= 3 or \
                    approach.LaneConfiguration is None:
                score = CROSS_NO_MED_TABLE[2][0]
            elif len(approach.LaneConfiguration) <= 5:
                score = CROSS_NO_MED_TABLE[2][1]
            else:
                score = CROSS_NO_MED_TABLE[2][2]
        else:
            if len(approach.LaneConfiguration) <= 3 or \
                    approach.LaneConfiguration is None:
                score = CROSS_NO_MED_TABLE[3][0]
            elif len(approach.LaneConfiguration) <= 5:
                score = CROSS_NO_MED_TABLE[3][1]
            else:
                score = CROSS_NO_MED_TABLE[3][2]

    return(score)



def _calculate_maxLane(laneConf):
    max_lane = 0
    if laneConf is None:
        max_lane = 1
    else:
        away_lane = len(laneConf[laneConf.find("X"):laneConf.rfind("X")+1])
        incomeing_lane = len(laneConf[laneConf.rfind("X")+1:])
        max_lane = max(away_lane, incomeing_lane)

    return(max_lane)



def calculate_unsignalizedCrossingWithMedian(self, field_name):
    score = 0
    streetintersectionapproach = "pcd.pcdqc.streetintersectionapproach_set"
    for approach in getattr(self, streetintersectionapproach):
        if approach.LaneConfiguration is None:
            continue
        maxLane = _calculate_maxLane(approach.LaneConfiguration)

        if self.PostedSpeed <= 25:
            if maxLane <= 2:
                score = CROSS_HAS_MED_TABLE[0][0]
            elif maxLane == 3:
                score = CROSS_HAS_MED_TABLE[0][1]
            else:
                score = CROSS_HAS_MED_TABLE[0][2]
        elif self.PostedSpeed == 30:
            if maxLane <= 2:
                score = CROSS_HAS_MED_TABLE[1][0]
            elif maxLane == 3:
                score = CROSS_HAS_MED_TABLE[1][1]
            else:
                score = CROSS_HAS_MED_TABLE[1][2]
        elif self.PostedSpeed == 35:
            if maxLane <= 2:
                score = CROSS_HAS_MED_TABLE[2][0]
            elif maxLane == 3:
                score = CROSS_HAS_MED_TABLE[2][1]
            else:
                score = CROSS_HAS_MED_TABLE[2][2]
        else:
            if maxLane <= 2:
                score = CROSS_HAS_MED_TABLE[3][0]
            elif maxLane == 3:
                score = CROSS_HAS_MED_TABLE[3][1]
            else:
                score = CROSS_HAS_MED_TABLE[3][2]

    return(score)



def calculate_BLTS(self, field_name):
    mixTraffic_score = calculate_mixTraffic(self, field_name)

    bikeLaneWithParking_score = calculate_bikeLaneWithParkingLane(self,
                                                                  field_name)

    bikeLaneWithoutParking_score = calculate_bikeLaneWithParkingLane(self,
                                                                     field_name)

    segment_score = aggreage_Score(mixTraffic_score,
                                   bikeLaneWithParking_score,
                                   bikeLaneWithoutParking_score, method="MIN")

    rtl_score = calculate_rightTurnLane(self, field_name)

    ltl_score = calculate_leftTurnLane(self, field_name)

    unsignalizedCrossingWithMedian_score = \
        calculate_unsignalizedCrossingWithMedian(self,field_name)

    unsignalizedCrossingWithoutMedian_score = \
        calculate_unsignalizedCrossingWithoutMedian(self, field_name)

    final_score = aggreage_Score(segment_score,
                                 rtl_score,
                                 ltl_score,
                                 unsignalizedCrossingWithMedian_score,
                                 unsignalizedCrossingWithoutMedian_score,
                                 method="MAX")

    print(final_score)
    return(final_score)

# Add the mixTraffic method to the Segment class.
Segment._calculate_BLTS = calculate_BLTS


# Override the BLTSScore field with a method field.
Segment.BLTSScore = MethodField(
    'BLTS Score',
    method_name='_calculate_BLTS'
)

# Clear the field cache.
del Segment._fields

# The newly-added field needs to be registered with the feature class.
layer_fields = Segment.workspace.get_layer_fields(Segment.name)
Segment.fields['BLTSScore'].register(
    Segment.workspace, Segment, 'BLTSScore', Segment.name, layer_fields)


if __name__ == "__main__":
    #with Segment.workspace.edit():
    if arcpy.CheckProduct("ArcInfo") != "Available":
        print("License Not Available")
        exit()
    else:
        print("License Available")

    with Segment.workspace.edit():
        for segment in Segment.objects.filter(InUrbanizedArea=D('Yes')):
            segment.BLTSScore
            segment.save()




