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
                              "sharrow",
                              "rtl",
                              "ltl"]
        self.scoreField = ["segmentScore"]


        self.mixTrafficField = ["SPEED", "lpd", self.analysisField[2]]
        self.combBikePkWidthField = ["lpd", "SPEED",
                                  "Comb_ParkBike_width", "HasParkingLane",
                                  self.analysisField[0]]
        self.blWithoutPkField = ["lpd", "SPEED",
                                 "Width", "HasParkLane",
                                 self.analysisField[1]]
        self.rtlField = [""]


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
        self.combBikePkWidthField = [lpd, speed, comb_pkbi_width,
                                     has_parking, self.analysisField[0]]


    def assignBLwithPkLane(self):
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
        self.blWithoutPkField = [lpd, speed,
                                 bl_width, has_parking,
                                 self.analysisField[1]]

    def assignBLwithoutPkLane(self):
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



def crop(in_feature, clip_feature, out_feature = None):
    if out_feature == None:
        out_feature == in_feature + "_cropped"

    arcpy.Clip_analysis(in_feature, clip_feature, out_feature)

    print("Finish clipping...")
    return(out_feature)


if __name__ == '__main__':

    #FC_NAME = crop(os.path.join(GDB_PATH, FC_NAME),
    #               "G:\Resources\Data\Boundary.gdb\UAB2013",
    #              os.path.join(GDB_PATH, "streetCL_cropped")
    #              )

    a = BLTS_Analysis(GDB_PATH, FC_NAME)
    a.deleteField()
    a.addField()
    a.setMixTrafficField("SPEED","lpd")
    a.assignMixTrafficScore()
    a.setPkLaneField("lpd", "SPEED", "Comb_ParkBike_width", "HasParkingLane")
    a.assignBLwithPkLane()
    a.setNoPkLaneField("lpd", "SPEED", "Width", "HasParkingLane")
    a.assignBLwithoutPkLane()
    a.aggregateSegmentScore()














