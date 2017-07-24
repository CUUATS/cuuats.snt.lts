import arcpy
import os

GDB_PATH = 'G:\CUUATS\Sustainable Neighborhoods Toolkit\Data\SustainableNeighborhoodsToolkit.gdb'
FC_NAME = 'streetCL_cropped'
FULL_PATH = os.path.join(GDB_PATH, FC_NAME)


class BLTS_Analysis(object):
    def __init__(self, GDB_PATH, FC_NAME):
        self.GBD_PATH = GDB_PATH
        self.FC_NAME = FC_NAME
        self.FULL_PATH = os.path.join(self.GBD_PATH, self.FC_NAME)
        self.analysisField = ["pkLane",
                              "noPkLane",
                              "mixTraffic",
                              "sharrow"]

        self.scoreField = ["segmentScore",
                           "rtlScore",
                           "ltlScore",
                           "unsignalized_NoMedian",
                           "unsignalized_Median",
                           "overallScore"]


        self.mixTrafficField = ["SPEED", "lpd", self.analysisField[2]]
        self.combBikePkWidthField = ["lpd", "SPEED",
                                  "Comb_ParkBike_width", "HasParkingLane",
                                  self.analysisField[0]]
        self.blWithoutPkField = ["lpd", "SPEED",
                                 "Width", "HasParkLane",
                                 self.analysisField[1]]
        self.rtlField = ["RTL_Conf_", "RTL_Len_",
                         "bike_AA_", self.scoreField[1]]
        self.ltlField = ["SPEED", "LTL_Conf_", "LTL_lanescrossed_",
                         self.scoreField[2]]
        self.unsignalized_NoMedianField = ["med_present", "SPEED",
                                           "TotalLanes_EW1", "TotalLanes_NS",
                                           "Control_Type",
                                           self.scoreField[3]]



        arcpy.env.workspace = GDB_PATH


    def getName(self):
        '''
        Get the name of GDB Path and Feature Class Path
        :return: 
        '''
        print(self.GBD_PATH, self.FC_NAME)


    def getFullPath(self):
        '''
        Get the full path of the feature class
        :return: 
        '''
        print(self.FULL_PATH)


    def addField(self):
        '''
        Add the fields that is used to contain the score 
        from the different part of the analysis
        :return: 
        '''
        for field in self.analysisField:
            arcpy.AddField_management(self.FC_NAME, field, "SHORT")
        for field in self.scoreField:
            arcpy.AddField_management(self.FC_NAME, field, "SHORT")
        print("Complete Adding Analysis Fields....")


    def deleteField(self):
        '''
        Delete all the fields that is used to from the 
        analysis fields
        :return: 
        '''
        for field in self.analysisField:
            arcpy.DeleteField_management(self.FC_NAME, field)
        for field in self.scoreField:
            arcpy.DeleteField_management(self.FC_NAME, field)
        print("Complete Delete Analysis Fields....")


    def setMixTrafficField(self, speed, lpd):
        """
        Point to the correct field for the mix traffic analysis
        :param speed: required a string of the speed field 
        :param lpd: required a string of the lane per direction field
        :return: 
        """
        self.mixTrafficField = [speed, lpd, self.analysisField[2]]


    def assignMixTrafficScore(self):
        """
        Assign mix traffic score based on scoring criteria
        TODO: Need to improve the way score is entered.
        :return: 
        """
        with arcpy.da.UpdateCursor(self.FC_NAME,
                                   self.mixTrafficField) as cursor:
            for row in cursor:
                ## Speed less than or equal to 25
                if row[0] <=  25:
                    if row[1] == 0:
                        row[2] = 1
                    elif row[1] == 1:
                        row[2] = 2
                    elif row[1] == 2:
                        row[2] = 3
                    else:
                        row[2] = 4

                ## Speed equal to 30
                if row[0] == 30:
                    if row[1] == 0:
                        row[2] = 2
                    elif row[1] == 1:
                        row[2] = 3
                    elif row[1] == 2:
                        row[2] = 4
                    else:
                        row[2] = 4

                ## Speed greater than 35
                if row[0] >= 35:
                    if row[1] == 0:
                        row[2] = 3
                    elif row[1] == 1:
                        row[2] = 4
                    elif row[1] == 2:
                        row[2] = 4
                    else:
                        row[2] = 4

                cursor.updateRow(row)

        print("Finish Mix Traffic Scoring")


    def setPkLaneField(self, lpd, speed, comb_pkbi_width, has_parking):
        """
        Point to the correct field for the bike lane with parking lane
        analysis
        :param lpd: required a string of the lane per direction field 
        :param speed: required a string of the speed field
        :param comb_pkbi_width: required a string of the combine parking
        with bike lane width field
        :param has_parking: required a strimg of the has parking field
        :return: 
        """
        self.combBikePkWidthField = [lpd, speed, comb_pkbi_width,
                                     has_parking, self.analysisField[0]]


    def assignBLwithPkLane(self):
        """
        Assign score for bike lane with parking lane criteria based on the 
        analysis field and write the score in the PkLane field in the 
        feature class
        :return: 
        """
        with arcpy.da.UpdateCursor(self.FC_NAME,
                                   self.combBikePkWidthField) as cursor:
            for row in cursor:
                ## Has adjacent Parking Lane
                if row[3] == 50:

                    # 1 LPD
                    if row[0] == 1 or row[0] == 0:

                        ## Speed 25
                        if row[1] <= 25:
                            if row[2] >= 15:
                                row[4] = 1
                            elif row[2] < 15 and row[2] > 13:
                                row[4] = 2
                            else:
                                row[4] = 3


                        ## Speed 30
                        elif row[1] == 30:
                            if row[2] >= 15:
                                row[4] = 1
                            elif row[2] < 15 and row[2] > 13:
                                row[4] = 2
                            else:
                                row[4] = 3

                        ## Speed 35
                        elif row[1] == 35:
                            if row[2] >= 15:
                                row[4] = 2
                            elif row[2] < 15 and row[2] > 13:
                                row[4] = 3
                            else:
                                row[4] = 3

                        ## Speed >= 40
                        else:
                            if row[2] >= 15:
                                row[4] = 2
                            elif row[2] < 15 and row[2] > 13:
                                row[4] = 4
                            else:
                                row[4] = 4

                    ## >= 2 LPD
                    if row[0] >= 2:
                        if row[1] <= 25:
                            if row[2] >= 15:
                                row[4] = 2
                            else:
                                row[4] = 3

                        elif row[1] == 30:
                            if row[2] >= 15:
                                row[4] = 2
                            else:
                                row[4] = 3

                        elif row[1] == 35:
                            if row[2] >= 15:
                                row[4] = 3
                            else:
                                row[4] = 3

                        else:
                            if row[2] >= 15:
                                row[4] = 3
                            else:
                                row[4] = 4

                cursor.updateRow(row)

        print("Finish BL with Parking Scoring")


    def setNoPkLaneField(self, lpd, speed, bl_width, has_parking):
        """
        Point to the correct field for the bike lane without adjacent parking
        :param lpd: required a string for the lane per direction field
        :param speed: required a string for speed field
        :param bl_width: required a string for bike lane width field
        :param has_parking: required a string for teh has parking field
        :return: 
        """
        self.blWithoutPkField = [lpd, speed,
                                 bl_width, has_parking,
                                 self.analysisField[1]]


    def assignBLwithoutPkLane(self):
        """
        Assign score for bike lane without parking lane criteria based on the 
        analysis field and write the score in the noPkLane field in the 
        feature class
        :return: 
        """
        with arcpy.da.UpdateCursor(self.FC_NAME,
                                   self.blWithoutPkField) as cursor:
            for row in cursor:
                ## Does not have adjacent Parking Lane
                if row[3] != 50 and row[2] >= 0:
                    ## 1 LPD
                    if row[0] == 1 or row[0] == 0:
                        ## Speed <= 30
                        if row[1] <= 30:
                            if row[2] >= 7:
                                row[4] = 1
                            elif row[2] < 7 and row[2] > 5.5:
                                row[4] = 1
                            else:
                                row[4] = 2

                        ## Speed 35
                        elif row[1] == 35:
                            if row[2] >= 7:
                                row[4] = 2
                            elif row[2] < 7 and row[2] > 5.5:
                                row[4] = 3
                            else:
                                row[4] = 3
                        ## Speed >= 40
                        else:
                            if row[2] >= 7:
                                row[4] = 3
                            elif row[2] < 7 and row[2] > 5.5:
                                row[4] = 4
                            else:
                                row[4] = 4

                    ## >= 2 LPD
                    if row[0] >= 2:
                        ## Speed <= 30
                        if row[1] <= 30:
                            if row[2] >= 7:
                                row[4] = 1
                            else:
                                row[4] = 3
                        ## Speed 35
                        elif row[1] == 35:
                            if row[2] >= 7:
                                row[4] = 2
                            else:
                                row[4] = 3
                        ## Speed >= 40
                        else:
                            if row[2] >= 7:
                                row[4] = 3
                            else:
                                row[4] = 4


                cursor.updateRow(row)

        print("Finish BL without Parking Scoring")


    def aggregateSegmentScore(self):
        """
        Based on the score generated by bike lane with adjacent parking /
        bike lane without adjacent parking / mix traffic score.  Based on these
        fields, they are aggregated based on the minimum of the three and
        write the score in the mix traffic field in the feature class
        :return: 
        """
        updateScoreField = [self.analysisField[0],
                            self.analysisField[1],
                            self.analysisField[2],
                            self.scoreField[0]]
        with arcpy.da.UpdateCursor(self.FC_NAME,
                                   updateScoreField) as cursor:
            for row in cursor:
                if row[0] == None:
                    row[0] = 99
                if row[1] == None:
                    row[1] = 99
                if row[2] == None:
                    row[2] = 99

                row[3] = min(row[:3])

                cursor.updateRow(row)


        print("Finish Aggregating Road Segment Score")


    def setRTLFiled(self, rtl_conf, rtl_len, bike_aa):
        """
        Point to the correct field for the RTL analysis, given that there are
        four directions for the approach.  The string that it will take are 
        the fields that it will take without the direction.  
        :param rtl_conf: required a string for the right turn lane 
        configuration, for example 'rtl_conf_'
        :param rtl_len: required a string for the right turn lane length
        :param bike_aa: required a string for the bike lane approach alignment
        :return: 
        """
        self.rtlField = [rtl_conf,
                         rtl_len,
                         bike_aa,
                         self.scoreField[1]]


    def assignRTL(self):
        directions = ["N", "S", "E", "W"]
        field_list = []
        for d in directions:
            for field in self.rtlField[:3]:
                field = field + d
                field_list.append(field)

            #code here
            field_list.append(self.scoreField[1])
            with arcpy.da.UpdateCursor(self.FC_NAME, field_list) as cursor:
                for row in cursor:
                    ## looking for any right turn lane configuration
                    if row[0] != 0:
                        ## single rtl conf
                        if row[0] == 1 and row[1] <= 150 and row[2] == 1:
                            row[3] = 2
                        if row[0] == 1 and row[1] > 150 and row[2] == 1:
                            row[3] = 3
                        if row[0] == 1 and row[2] == 2:
                            row[3] = 3
                        if row[0] == 2:
                            row[3] = 4

                    cursor.updateRow(row)

            field_list = []
        print("Finish assigning to Right Turn Lane Criteria...")


    def setLTLField(self, speed, ltl_conf, ltl_lanecrossed):
        self.ltlField = [speed,
                         ltl_conf,
                         ltl_lanecrossed,
                         self.scoreField[2]]


    def assignLTL(self):
        directions = ["N", "S", "E", "W"]
        field_list = []
        for d in directions:
            field_list.append(self.ltlField[0])
            for field in self.ltlField[1:3]:
                field = field + d
                field_list.append(field)
            field_list.append(self.ltlField[3])


            #code here
            with arcpy.da.UpdateCursor(self.FC_NAME, field_list) as cursor:
                for row in cursor:
                    if row[1] and row[2] != 0:
                        # Dual Exclusive
                        if row[1] != 0:
                            row[3] = 4

                        # Speed less than 25
                        elif row[0] <= 25:
                            if row[2] == 0:
                                row[3] = 2
                            elif row[2] == 1:
                                row[3] = 2
                            elif row[2] >= 2:
                                row[3] = 3

                        # Speed 30
                        elif row[0] <= 25:
                            if row[2] == 0:
                                row[3] = 2
                            elif row[2] == 1:
                                row[3] = 3
                            elif row[2] >= 2:
                                row[3] = 4

                        # Speed greater than 35
                        elif row[0] <= 25:
                            if row[2] == 0:
                                row[3] = 3
                            elif row[2] == 1:
                                row[3] = 4
                            elif row[2] >= 2:
                                row[3] = 4

                    cursor.updateRow(row)

            field_list = []
        print("Finish assigning score to Left Turn Lane Criteria...")


    def aggregate_OverallScore(self):
        with arcpy.da.UpdateCursor(FC_NAME, self.scoreField) as cursor:
            for row in cursor:
                row[5] = max(row[:6])

                cursor.updateRow(row)

        print("Finish aggregating the overall score")



    def setUnsignalizedNoMedianField(self, med_present, speed,
                                     total_lanes_EW,
                                     total_lanes_NS,
                                     control_type):

        self.unsignalized_NoMedianField = [med_present, speed,
                                           total_lanes_EW,
                                           total_lanes_NS,
                                           control_type,
                                           self.scoreField[3]]


    def assignUnsignalized_NoMedian(self):
        with arcpy.da.UpdateCursor(FC_NAME,
                                   self.unsignalized_NoMedianField)as cursor:
            for row in cursor:
                maxLane = max(row[2:4])
                if row[4] != "Signal":
                    if row[0] == "No":
                        if row[1] <= 25:
                            if maxLane <= 3:
                                row[5] = 1
                            elif maxLane == 4 or 5:
                                row[5] = 2
                            else:
                                row[5] = 4

                        elif row[1] == 30:
                            if maxLane <= 3:
                                row[5] = 1
                            elif maxLane == 4 or 5:
                                row[5] = 2
                            else:
                                row[5] = 4

                        elif row[1] == 35:
                            if maxLane <= 3:
                                row[5] = 2
                            elif maxLane == 4 or 5:
                                row[5] = 3
                            else:
                                row[5] = 4

                        else:
                            if maxLane <= 3:
                                row[5] = 3
                            elif maxLane == 4 or 5:
                                row[5] = 4
                            else:
                                row[5] = 4

                cursor.updateRow(row)

        print("Finish calculating unsginalized crossing with no median...")



    def calculate_AllScore(self):
        """
        Calculate the score for mix traffic, bike lane with parking lane,
        bike lane without parking lane.  Then aggregate the score of the 
        general segment condition. Calculate the score for right turn lane and
        left turn lane criteria.  Aggregate the segment score into an overall
        score. 
        :return: score written in the corresponding field in the feature class 
        """
        self.assignMixTrafficScore()
        self.assignBLwithPkLane()
        self.assignBLwithoutPkLane()
        self.aggregateSegmentScore()
        self.assignRTL()
        self.assignLTL()
        self.assignUnsignalized_NoMedian()
        self.aggregate_OverallScore()



def crop(in_feature, clip_feature, out_feature = None):
    """
    This function helps with cropping the street layer before analysis
    :param in_feature: Name of street feature classs
    :param clip_feature: Name of border feature class
    :param out_feature: Name of cropped street feature class
    :return: Name of cropped street feature class
    """
    if out_feature == None:
        out_feature = in_feature + "_cropped"

    arcpy.Clip_analysis(in_feature, clip_feature, out_feature)

    print("Finish clipping...")
    return(out_feature)


if __name__ == '__main__':
    a = BLTS_Analysis(GDB_PATH, FC_NAME)
    a.deleteField()
    a.addField()
    a.setMixTrafficField("SPEED","lpd")
    a.setPkLaneField("lpd", "SPEED", "Comb_ParkBike_width", "HasParkingLane")
    a.setNoPkLaneField("lpd", "SPEED", "Width", "HasParkingLane")
    a.setRTLFiled("RTL_Conf_", "RTL_len_", "bike_AA_")
    a.setLTLField("SPEED", "LTL_Conf_", "LTL_lanescrossed_")
    a.setUnsignalizedNoMedianField("med_present", "SPEED", "TotalLanes_EW_12",
                                   "TotalLanes_NS", "Control_Type")
    a.calculate_AllScore()















