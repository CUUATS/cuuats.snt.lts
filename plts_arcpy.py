# plts_arcpy.py
# This script uses the arcpy library to calculate the PLTS score for
# each sidewalk segment and write the result in ArcGIS feature class
# Library required: arcpy

import arcpy
import os
from config import SW_COND_TABLE


class PLTS_Analysis(object):
    def __init__(self, GDB_PATH, FC_NAME):
        self.GBD_PATH = GDB_PATH
        self.FC_NAME = FC_NAME
        self.FULL_PATH = os.path.join(self.GBD_PATH, self.FC_NAME)
        self.scoreFields = ["swCondScore"]
        self._setupFields()

    def _setupFields(self):
        fc_fields = arcpy.ListFields(self.FULL_PATH)
        fc_field_list = [field.name for field in fc_fields]

        for scoreField in self.scoreFields:
            if scoreField in fc_field_list:
                with arcpy.da.UpdateCursor(self.FULL_PATH,
                                           scoreField) as cursor:
                    for row in cursor:
                        row[0] = None
                        cursor.updateRow(row)

            else:
                arcpy.AddField_management(self.FULL_PATH,
                                          scoreField,
                                          "SHORT")


    def assignSidewalkCondScore(self, sw_width = None, sw_cond = None):
        if not sw_cond or not sw_width:
            raise ValueError("Sidewalk Width and Sidewalk "
                                "Condition must be entered")

        field_names = [sw_width, sw_cond, self.scoreFields[0]]
        with arcpy.da.UpdateCursor(self.FULL_PATH, field_names) as cursor:
            for row in cursor:
                # Less than 4 feet of sidewalk
                if row[0] == None:
                    row[2] = 4
                elif row[0] / 12 < 4:
                    if row[1] == "Good":
                        row[2] = SW_COND_TABLE[0][0]
                    elif row[1] == "Fair":
                        row[2] = SW_COND_TABLE[0][1]
                    elif row[1] == "Poor":
                        row[2] = SW_COND_TABLE[0][2]
                    elif row[1] == "Very Poor":
                        row[2] = SW_COND_TABLE[0][3]
                    else:
                        row[2] = SW_COND_TABLE[0][4]
                # Between 4 to 5 feet of sidewalk
                elif row[0] / 12 >= 4 and row[0] / 12 < 5:
                    if row[1] == "Good":
                        row[2] = SW_COND_TABLE[1][0]
                    elif row[1] == "Fair":
                        row[2] = SW_COND_TABLE[1][1]
                    elif row[1] == "Poor":
                        row[2] = SW_COND_TABLE[1][2]
                    elif row[1] == "Very Poor":
                        row[2] = SW_COND_TABLE[1][3]
                    else:
                        row[2] = SW_COND_TABLE[1][4]
                # Between 5 to 6 feet of sidewalk
                elif row[0] / 12 >= 5 and row[0] / 12 < 6:
                    if row[1] == "Good":
                        row[2] = SW_COND_TABLE[2][0]
                    elif row[1] == "Fair":
                        row[2] = SW_COND_TABLE[2][1]
                    elif row[1] == "Poor":
                        row[2] = SW_COND_TABLE[2][2]
                    elif row[1] == "Very Poor":
                        row[2] = SW_COND_TABLE[2][3]
                    else:
                        row[2] = SW_COND_TABLE[2][4]
                # Greater than 6 feet of sidewalk
                else:
                    if row[1] == "Good":
                        row[2] = SW_COND_TABLE[3][0]
                    elif row[1] == "Fair":
                        row[2] = SW_COND_TABLE[3][1]
                    elif row[1] == "Poor":
                        row[2] = SW_COND_TABLE[3][2]
                    elif row[1] == "Very Poor":
                        row[2] = SW_COND_TABLE[3][3]
                    else:
                        row[2] = SW_COND_TABLE[3][4]

                cursor.updateRow(row)


def convertScoreCategory(fc_path, inputField,
                         outputField = "CondScoreCat"):
    fc_fields = arcpy.ListFields(fc_path)
    fc_field_list = [field.name for field in fc_fields]

    if outputField in fc_field_list:
        with arcpy.da.UpdateCursor(fc_path, outputField) as cursor:
            for row in cursor:
                row[0] = None
                cursor.updateRow(row)
    else:
        arcpy.AddField_management(fc_path,
                                  outputField,
                                  "TEXT",
                                  10)

    convert_list = [inputField, outputField]
    with arcpy.da.UpdateCursor(fc_path, convert_list) as cursor:
        for row in cursor:
            if row[0] >= 90:
                row[1] = "Good"
            elif row[0] >= 80:
                row[1] = "Fair"
            elif row[0] >= 70:
                row[1] = "Poor"
            else:
                row[1] = "Very Poor"

            cursor.updateRow(row)


    return(outputField)


def main():
    GDB_PATH = "C:\Users\kml42638\Desktop\TestDB.gdb"
    FC_NAME = "sidewalk"

    convertScoreCategory(fc_path=os.path.join(GDB_PATH, FC_NAME),
                         inputField="ScoreCondition")

    a = PLTS_Analysis(GDB_PATH, FC_NAME)
    a.assignSidewalkCondScore(sw_cond = "CondScoreCat",
                              sw_width = "Width")


if __name__ == "__main__":
    main()
