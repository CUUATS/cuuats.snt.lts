# blts_arcpy.py
# This script uses the arcpy library to calculate the BLTS score for
# each road segment and write the result in ArcGIS feature class
# Library required: arcpy

import arcpy
import os
import numpy as np
from config import BL_ADJ_PK_TABLE, BL_NO_ADJ_PK_TABLE, MIXED_TRAF_TABLE, \
    RTL_CRIT_TABLE, LTL_CRIT_TABLE, CROSS_NO_MED_TABLE, CROSS_HAS_MED_TABLE


class BLTS_Analysis(object):
    def __init__(self, GDB_PATH, FC_NAME):
        self.GBD_PATH = GDB_PATH
        self.FC_NAME = FC_NAME
        self.FC_PATH = os.path.join(self.GBD_PATH, self.FC_NAME)
        self.scoreFields = ["bikeLaneWithPkLane",
                            "bikeLaneNoPkLane",
                            "mixTraffic",
                            "sharrow",
                            "segmentScore",
                            "rtlScore",
                            "ltlScore",
                            "unsignalized_NoMedian",
                            "unsignalized_HasMedian",
                            "overallScore"]


    def _setupFields(self, scoreField, checklist):
        """
        This internal method checks rather the scoreField which is used to
        contain the score exist, if the field already exisit, it will update to
        previous values to zero.  If the field doesn't exist, it will add a 
        field in the future class.
        
        It will use the checklist parameter, which are the input fields for the
        analysis, and check rather the fields exist in the future class.  If 
        they do not exist, it will raise an error.
        :param scoreField: Field that is used to contain the score for each 
        segment
        :param checklist: List of fields that is used for the analysis
        :return: output score is written in the future class
        """
        fc_fields = arcpy.ListFields(self.FC_PATH)
        fc_field_list = [field.name for field in fc_fields]

        for field in checklist:
            if field not in fc_field_list:
                raise NameError("{} is not found".format(field))


        if scoreField in fc_field_list:
            with arcpy.da.UpdateCursor(self.FC_PATH, scoreField) as cursor:
                for row in cursor:
                    row[0] = None
                    cursor.updateRow(row)

        else:
            arcpy.AddField_management(self.FC_PATH,
                                      scoreField,
                                      "SHORT")



    def assingBLwithPkLaneScore(self, lane_Per_Dir = None, speed = None,
                           comb_PkBike_Width = None, has_Parking = None):
        """
        This method allows the users to assign bike lane with parking lane score
        based on the blts method.  It takes in all the criteria as string and 
        output and interger score in the input future class. 
        :param lane_Per_Dir: string name for the field in the future class that 
        contain lane per direction data
        :param speed: string name for the field in the future class that 
        contain speed data
        :param comb_PkBike_Width: string name for the field in the future class 
        that contain combine parking and bike lane width data
        :param has_Parking: string name for the field in the future class that 
        contain has parking data
        :return: output score is written in the future class
        """
        if not lane_Per_Dir or not speed \
            or not comb_PkBike_Width or not has_Parking:
            raise ValueError("Lane per direction, speed, "
                             "comb parking bike width and has parking must be "
                             "entered")
        self._setupFields(self.scoreFields[0], [lane_Per_Dir,
                                                speed,
                                                comb_PkBike_Width,
                                                has_Parking])

        field_names = [lane_Per_Dir, speed, comb_PkBike_Width, has_Parking,
                       self.scoreFields[0]]

        with arcpy.da.UpdateCursor(self.FC_PATH, field_names) as cursor:
            for row in cursor:
                ## Has adjacent Parking Lane
                if row[3] == 50:
                    # 1 LPD
                    if row[0] == 1 or row[0] == 0:
                        ## Speed 25
                        if row[1] <= 25:
                            if row[2] >= 15:
                                row[4] = BL_ADJ_PK_TABLE[0][0]
                            elif row[2] < 15 and row[2] > 13:
                                row[4] = BL_ADJ_PK_TABLE[0][1]
                            else:
                                row[4] = BL_ADJ_PK_TABLE[0][2]


                        ## Speed 30
                        elif row[1] == 30:
                            if row[2] >= 15:
                                row[4] = BL_ADJ_PK_TABLE[1][0]
                            elif row[2] < 15 and row[2] > 13:
                                row[4] = BL_ADJ_PK_TABLE[1][1]
                            else:
                                row[4] = BL_ADJ_PK_TABLE[1][2]

                        ## Speed 35
                        elif row[1] == 35:
                            if row[2] >= 15:
                                row[4] = BL_ADJ_PK_TABLE[2][0]
                            elif row[2] < 15 and row[2] > 13:
                                row[4] = BL_ADJ_PK_TABLE[2][1]
                            else:
                                row[4] = BL_ADJ_PK_TABLE[2][2]

                        ## Speed >= 40
                        else:
                            if row[2] >= 15:
                                row[4] = BL_ADJ_PK_TABLE[3][0]
                            elif row[2] < 15 and row[2] > 13:
                                row[4] = BL_ADJ_PK_TABLE[3][1]
                            else:
                                row[4] = BL_ADJ_PK_TABLE[3][2]

                    ## >= 2 LPD
                    elif row[0] >= 2:
                        if row[1] <= 25:
                            if row[2] >= 15:
                                row[4] = BL_ADJ_PK_TABLE[0][3]
                            else:
                                row[4] = BL_ADJ_PK_TABLE[0][4]

                        elif row[1] == 30:
                            if row[2] >= 15:
                                row[4] = BL_ADJ_PK_TABLE[1][3]
                            else:
                                row[4] = BL_ADJ_PK_TABLE[1][4]

                        elif row[1] == 35:
                            if row[2] >= 15:
                                row[4] = BL_ADJ_PK_TABLE[2][3]
                            else:
                                row[4] = BL_ADJ_PK_TABLE[2][4]

                        else:
                            if row[2] >= 15:
                                row[4] = BL_ADJ_PK_TABLE[3][3]
                            else:
                                row[4] = BL_ADJ_PK_TABLE[3][4]

                cursor.updateRow(row)



    def assignBLwithoutPkLaneScore(self, lane_Per_Dir = None, speed = None,
                              bikeLane_width = None, has_Parking = None):
        """
        This method allows the users to assign bike lane without parking lane 
        score based on the blts method.  It takes in all the criteria as string 
        and output and interger score in the input future class. 
        :param lane_Per_Dir: string name for the field in the future class that 
        contain lane per direction data
        :param speed: string name for the field in the future class that 
        contain speed data
        :param bikeLane_width: string name for the field in the future class that 
        contain bike lane width data
        :param has_Parking: string name for the field in the future class that 
        contain has parking data
        :return: output score is written in the future class
        """
        if not lane_Per_Dir or not speed \
            or not bikeLane_width or not has_Parking:
            raise ValueError("Lane per direction, speed, "
                             "bike lane width and has parking must be "
                             "entered")
        self._setupFields(self.scoreFields[1], [lane_Per_Dir,
                                                speed,
                                                bikeLane_width,
                                                has_Parking])

        field_names = [lane_Per_Dir, speed, bikeLane_width, has_Parking,
                       self.scoreFields[1]]

        with arcpy.da.UpdateCursor(self.FC_PATH, field_names) as cursor:
            for row in cursor:
                ## Does not have adjacent Parking Lane
                if row[3] != 50 and row[2] >= 0:
                    ## 1 LPD
                    if row[0] == 1 or row[0] == 0:
                        ## Speed <= 30
                        if row[1] <= 30:
                            if row[2] >= 7:
                                row[4] = BL_NO_ADJ_PK_TABLE[0][0]
                            elif row[2] < 7 and row[2] > 5.5:
                                row[4] = BL_NO_ADJ_PK_TABLE[0][1]
                            else:
                                row[4] = BL_NO_ADJ_PK_TABLE[0][2]

                        ## Speed 35
                        elif row[1] == 35:
                            if row[2] >= 7:
                                row[4] = BL_NO_ADJ_PK_TABLE[1][0]
                            elif row[2] < 7 and row[2] > 5.5:
                                row[4] = BL_NO_ADJ_PK_TABLE[1][1]
                            else:
                                row[4] = BL_NO_ADJ_PK_TABLE[1][2]
                        ## Speed >= 40
                        else:
                            if row[2] >= 7:
                                row[4] = BL_NO_ADJ_PK_TABLE[2][0]
                            elif row[2] < 7 and row[2] > 5.5:
                                row[4] = BL_NO_ADJ_PK_TABLE[2][1]
                            else:
                                row[4] = BL_NO_ADJ_PK_TABLE[1][2]

                    ## >= 2 LPD
                    if row[0] >= 2:
                        ## Speed <= 30
                        if row[1] <= 30:
                            if row[2] >= 7:
                                row[4] = BL_NO_ADJ_PK_TABLE[0][4]
                            else:
                                row[4] = BL_NO_ADJ_PK_TABLE[0][5]
                        ## Speed 35
                        elif row[1] == 35:
                            if row[2] >= 7:
                                row[4] = BL_NO_ADJ_PK_TABLE[1][4]
                            else:
                                row[4] = BL_NO_ADJ_PK_TABLE[1][5]
                        ## Speed >= 40
                        else:
                            if row[2] >= 7:
                                row[4] = BL_NO_ADJ_PK_TABLE[2][4]
                            else:
                                row[4] = BL_NO_ADJ_PK_TABLE[2][5]

                cursor.updateRow(row)


    def assignMixTrafficScore(self, speed = None, lane_per_dir = None):
        """
        This method allows the users to assign mix traffic score based on the 
        blts method.  It takes in all the criteria as string and output and 
        interger score in the input future class. 
        :param speed: string name for the field in the future class that 
        contain speed data
        :param lane_per_dir: string name for the field in the future class that 
        contain lane per direction data
        :return: output score is written in the future class
        """
        if not speed or not lane_per_dir:
            raise ValueError("Speed and lane per direction must be entered")
        self._setupFields(self.scoreFields[2], checklist=[speed, lane_per_dir])

        field_names = [speed, lane_per_dir, self.scoreFields[2]]
        with arcpy.da.UpdateCursor(self.FC_PATH,
                                   field_names) as cursor:
            for row in cursor:
                ## Speed less than or equal to 25
                if row[0] <=  25:
                    if row[1] == 0:
                        row[2] = MIXED_TRAF_TABLE[0][0]
                    elif row[1] == 1:
                        row[2] = MIXED_TRAF_TABLE[0][1]
                    elif row[1] == 2:
                        row[2] = MIXED_TRAF_TABLE[0][2]
                    else:
                        row[2] = MIXED_TRAF_TABLE[0][3]

                ## Speed equal to 30
                elif row[0] == 30:
                    if row[1] == 0:
                        row[2] = MIXED_TRAF_TABLE[1][0]
                    elif row[1] == 1:
                        row[2] = MIXED_TRAF_TABLE[1][1]
                    elif row[1] == 2:
                        row[2] = MIXED_TRAF_TABLE[1][2]
                    else:
                        row[2] = MIXED_TRAF_TABLE[1][3]

                ## Speed greater than 35
                else:
                    if row[1] == 0:
                        row[2] = MIXED_TRAF_TABLE[2][0]
                    elif row[1] == 1:
                        row[2] = MIXED_TRAF_TABLE[2][1]
                    elif row[1] == 2:
                        row[2] = MIXED_TRAF_TABLE[2][2]
                    else:
                        row[2] = MIXED_TRAF_TABLE[2][3]

                cursor.updateRow(row)



    def aggregateSegmentScore(self, method = "MIN"):
        """
        This method allows the user to combine the score of bike Lane with
        parking lane, bike lane without parking lane and general mix traffic 
        score into combine score. 
        :param method: Optional: Choosing the aggregation method, default is 
        using the minimal of the three, other options are "AVG' and 'MAX'
        :return: the aggregated scored is written in the future class
        """

        self._setupFields(self.scoreFields[4], [self.scoreFields[0],
                                                self.scoreFields[1],
                                                self.scoreFields[2]])

        field_names = [self.scoreFields[0],
                       self.scoreFields[1],
                       self.scoreFields[2],
                       self.scoreFields[4]]

        with arcpy.da.UpdateCursor(self.FC_PATH, field_names) as cursor:
            for row in cursor:
                if row[0] == None:
                    row[0] = 99
                if row[1] == None:
                    row[1] = 99
                if row[2] == None:
                    row[2] = 99
                if method == "MIN":
                    row[3] = min(row[:3])
                if method == "MAX":
                    row[3] = max(row[:3])
                if method == "AVG":
                    row[3] = round(np.mean(row[:3]))

                cursor.updateRow(row)



    def assignRightTurnLaneScore(self, rtl_conf = None, rtl_len = None,
                                 bike_aa = None):
        """
        This method allows the users to assign right turn lane score based on 
        the blts method.  It takes in all the criteria as string and output and 
        interger score in the input future class.
        :param rtl_conf: string name for the field in the future class that 
        contain right turn lane configuration data
        :param rtl_len: string name for the field in the future class that 
        contain right turn lane length data
        :param bike_aa: string name for the field in the future class that 
        contain bike lane approach alignment data
        :return: score is written in the input future class
        """
        if not rtl_conf or not rtl_len or not bike_aa:
            raise ValueError("Right turn lane configuration, " 
                             "right turn lane length and "
                             "bike lane approach alignment must be entered")

        input_field = [rtl_conf, rtl_len, bike_aa]
        directions = ["N", "S", "E", "W"]
        field_names = []
        for d in directions:
            for field in input_field[:3]:
                field = field + d
                field_names.append(field)
        self._setupFields(self.scoreFields[5], field_names)

        field_names = []
        for d in directions:
            for field in input_field[:3]:
                field = field + d
                field_names.append(field)

            field_names.append(self.scoreFields[5])
            with arcpy.da.UpdateCursor(self.FC_PATH, field_names) as cursor:
                for row in cursor:
                    # looking for any right turn lane configuration
                    if row[0] != 0:
                        ## Check for first row
                        if row[0] == 1 and row[1] <= 150 and row[2] == 1:
                            if row[3] == None or row[3] < 2:
                                row[3] = RTL_CRIT_TABLE[0]

                        ## Check for second row
                        elif row[0] == 1 and row[1] >= 150 and row[2] == 1:
                            if row[3] == None or row[3] < 3:
                                row[3] = RTL_CRIT_TABLE[1]

                        ## Check for third row
                        elif row[0] == 1 and row[2] == 4:
                            if row[3] == None or row[3] < 3:
                                row[3] = RTL_CRIT_TABLE[2]

                        ## Check for fourth row
                        else:
                            row[3] = RTL_CRIT_TABLE[3]

                    cursor.updateRow(row)
            field_names = []


    def assignLeftTurnLaneScore(self, speed = None,
                                ltl_conf = None,
                                ltl_lanescrossed = None):
        """
        This method allows the users to assign left turn lane score based on 
        the blts method.  It takes in all the criteria as string and output and 
        interger score in the input future class.
        :param speed: string name for the field in the future class that 
        contain speed data
        :param ltl_conf: string name for the field in the future class that 
        contain left turn lane configuration data
        :param ltl_lanescrossed: string name for the field in the future class 
        that contain left turn lane lanes crossed data
        :return: score is written in the input future class
        """
        if not speed or not ltl_conf or not ltl_lanescrossed:
            raise ValueError("Speed, Left turn lane configuration, " 
                             "left turn lane lanes crossed must be entered")

        input_field = [speed, ltl_conf, ltl_lanescrossed]
        directions = ["N", "S", "E", "W"]
        field_names = []
        for d in directions:
            for field in input_field[1:3]:
                field = field + d
                field_names.append(field)
        field_names.append(speed)
        self._setupFields(self.scoreFields[6], field_names)

        field_names = []
        for d in directions:
            for field in input_field[1:3]:
                field = field + d
                field_names.append(field)
            field_names.append(speed)
            field_names.append(self.scoreFields[6])
            print(field_names)

            with arcpy.da.UpdateCursor(self.FC_PATH, field_names) as cursor:
                for row in cursor:
                    # All types of left turn lane configuration
                    if row[0] != 0:
                        if row[2] <= 25:
                            if row[3] == None or row[3] < 4:
                                row[3] = LTL_CRIT_TABLE[0][3]
                        elif row[2] == 30:
                            if row[3] == None or row[3] < 4:
                                row[3] = LTL_CRIT_TABLE[1][3]
                        else:
                            if row[3] == None or row[3] < 4:
                                row[3] = LTL_CRIT_TABLE[2][3]
                    # No left turn lane

                    else:
                        ## Speed less than 25
                        if row[2] <= 25:
                            ### no lanes crossed
                            if row[1] == 0:
                                if row[3] < 2:
                                    row[3] = LTL_CRIT_TABLE[0][0]
                            ### 1 lane crossed
                            if row[1] == 1:
                                if row[3] < 2:
                                    row[3] = LTL_CRIT_TABLE[0][1]
                            ### 2+ lanes crossed
                            if row[1] >= 2:
                                if row[3] < 3:
                                    row[3] = LTL_CRIT_TABLE[0][2]
                        ## Speed 30
                        elif row[2] == 30:
                            ### no lanes crossed
                            if row[1] == 0:
                                if row[3] < 2:
                                    row[3] = LTL_CRIT_TABLE[1][0]
                            ### 1 lane crossed
                            if row[1] == 1:
                                if row[3] < 3:
                                    row[3] = LTL_CRIT_TABLE[1][1]

                            ### 2+ lanes crossed
                            if row[1] >= 2:
                                if row[3] < 4:
                                    row[3] = LTL_CRIT_TABLE[1][2]
                        ## Speed >= 35
                        else:
                            ### no lanes crossed
                            if row[1] == 0:
                                if row[3] < 3:
                                    row[3] = LTL_CRIT_TABLE[2][0]
                            ### 1 lane crossed
                            if row[1] == 1:
                                if row[3] < 3:
                                    row[3] = LTL_CRIT_TABLE[2][1]

                            ### 2+ lanes crossed
                            if row[1] >= 2:
                                if row[3] < 4:
                                    row[3] = LTL_CRIT_TABLE[2][2]

                    cursor.updateRow(row)
            field_names = []


    def assignUnsignalizedNoMedianScore(self, med_present = None,
                                        speed = None,
                                        total_lanes_EW = None,
                                        total_lanes_NS = None,
                                        control_type = None):
        """
        This method allows the users to assign unsignalized with no median present crossing
        based on the blts method.  It takes in all the criteria as string and 
        output and interger score in the input future class.
        :param med_present: string name for the median present field
        :param speed: string name for the speed field
        :param total_lanes_EW: string name for the total lanes East/West field
        :param total_lanes_NS: string name for the total lanes North/South field
        :param control_type: string name for the control type field
        :return: score is written in the input future class
        """
        if not med_present or not speed or not total_lanes_EW \
                or not total_lanes_NS or not control_type:
            raise ValueError("Median present, speed, total lanes East/West " 
                             "total lanes North/South, and control type "
                             "must be entered")

        field_names = [med_present, speed,
                       total_lanes_EW, total_lanes_NS, control_type,
                       self.scoreFields[7]]
        self._setupFields(self.scoreFields[7], field_names)

        with arcpy.da.UpdateCursor(self.FC_PATH,
                                   field_names) as cursor:
            for row in cursor:
                maxLane = max(row[2:4])
                if row[4] != "Signal":
                    if row[0] == "No":
                        if row[1] <= 25:
                            if maxLane <= 3:
                                row[5] = CROSS_NO_MED_TABLE[0][0]
                            elif maxLane == 4 or maxLane == 5:
                                row[5] = CROSS_NO_MED_TABLE[0][1]
                            else:
                                row[5] = CROSS_NO_MED_TABLE[0][2]

                        elif row[1] == 30:
                            if maxLane <= 3:
                                row[5] = CROSS_NO_MED_TABLE[1][0]
                            elif maxLane == 4 or maxLane == 5:
                                row[5] = CROSS_NO_MED_TABLE[1][1]
                            else:
                                row[5] = CROSS_NO_MED_TABLE[1][2]

                        elif row[1] == 35:
                            if maxLane <= 3:
                                row[5] = CROSS_NO_MED_TABLE[2][0]
                            elif maxLane == 4 or maxLane == 5:
                                row[5] = CROSS_NO_MED_TABLE[2][1]
                            else:
                                row[5] = CROSS_NO_MED_TABLE[2][2]

                        else:
                            if maxLane <= 3:
                                row[5] = CROSS_NO_MED_TABLE[3][0]
                            elif maxLane == 4 or maxLane == 5:
                                row[5] = CROSS_NO_MED_TABLE[3][1]
                            else:
                                row[5] = CROSS_NO_MED_TABLE[3][2]

                cursor.updateRow(row)


    def assignUnsignalizedHasMedianScore(self, med_present, speed,
                                         through_lanes_EW, through_lanes_NS,
                                         control_type):
        if not med_present or not speed or not through_lanes_EW \
                or not through_lanes_NS or not control_type:
            raise ValueError("Median present, speed, through lanes East/West "
                             "through lanes North/South, and control type "
                             "must be entered")

        field_names = [med_present, speed,
                       through_lanes_EW, through_lanes_NS, control_type]
        self._setupFields(self.scoreFields[8], field_names)
        field_names.append(self.scoreFields[8])
        with arcpy.da.UpdateCursor(self.FC_PATH, field_names) as cursor:
            for row in cursor:
                maxLane = max(row[2:4])
                if row[4] != "Signal":
                    if row[0] == "Yes":
                        if row[1] <= 25:
                            if maxLane == 1 or 2:
                                row[5] = 1
                            elif maxLane == 3 or 4:
                                row[5] = 1
                            else:
                                row[5] = 2

                        elif row[1] == 30:
                            if maxLane == 1 or 2:
                                row[5] = 1
                            elif maxLane == 3 or 4:
                                row[5] = 2
                            else:
                                row[5] = 3

                        elif row[1] == 35:
                            if maxLane == 1 or 2:
                                row[5] = 2
                            elif maxLane == 3 or 4:
                                row[5] = 3
                            else:
                                row[5] = 4

                        else:
                            if maxLane == 1 or 2:
                                row[5] = 3
                            elif maxLane == 3 or 4:
                                row[5] = 4
                            else:
                                row[5] = 4

                cursor.updateRow(row)



    def aggregateOverallScore(self, fields, method = "MAX"):
        """
        This method allows for aggregation of the overall score based on the
        field of input 
        :param fields: list of input fields where the users want the score to
        be aggregated
        :param method: method using Maximum of all fields
        :return: score written in the overallScore field
        """
        self._setupFields(self.scoreFields[9], fields)
        if method == "MAX":
            fields.append(self.scoreFields[9])
            with arcpy.da.UpdateCursor(self.FC_PATH, fields) as cursor:
                for row in cursor:
                    row[-1] = max(row[:-1])
                    cursor.updateRow(row)


def main():
    GDB_PATH = r'G:\CUUATS\Sustainable Neighborhoods Toolkit\Data' \
    '\SustainableNeighborhoodsToolkit.gdb'
    FC_NAME = 'streeCL_cropped2'
    blts = BLTS_Analysis(GDB_PATH, FC_NAME)
    blts.assignMixTrafficScore("SPEED", "lpd")
    blts.assingBLwithPkLaneScore("lpd", "SPEED",
                            "Comb_ParkBike_width", "HasParkingLane")
    blts.assignBLwithoutPkLaneScore("lpd", "SPEED", "Width", "HasParkingLane")
    blts.aggregateSegmentScore()

    blts.assignRightTurnLaneScore("RTL_Conf_", "RTL_Len_", "bike_AA_")
    blts.assignLeftTurnLaneScore("SPEED", "LTL_Conf_", "LTL_lanescrossed_")
    blts.assignUnsignalizedNoMedianScore("med_present", "SPEED",
                                         "TotalLanes_EW_12", "TotalLanes_NS",
                                         "Control_Type")
    #blts.assignUnsignalizedHasMedianScore("med_present", "SPEED",
    #                                     "through_lane_EW", "through_lane_NS",
    #                                    "Control_Type")
    blts.aggregateOverallScore(["segmentScore",
                                "rtlScore",
                                "ltlScore",
                                "unsignalized_NoMedian"])

if __name__ == "__main__":
    main()















