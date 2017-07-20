import arcpy
import os
from cuuats.datamodel import feature_class_factory as factory

GDB_PATH = 'C:\Users\kml42638\Desktop\TestDB.gdb'
FC_NAME = 'Test_CL'
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
        self.mixTrafficField = ["SPEED", "lpd", self.analysisField[2]]
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
        print("Complete Adding Analysis Fields....")


    def deleteField(self):
        '''
        Delete all the fields that is used to from the 
        analysis fields
        :return: 
        '''
        for field in self.analysisField:
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



if __name__ == '__main__':
    a = BLTS_Analysis(GDB_PATH, FC_NAME)
    a.deleteField()
    a.addField()
    a.setMixTrafficField("SPEED","lpd")
    a.assignMixTrafficScore()













