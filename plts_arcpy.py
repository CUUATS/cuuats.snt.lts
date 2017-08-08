# plts_arcpy.py
# This script uses the arcpy library to calculate the PLTS score for
# each sidewalk segment and write the result in ArcGIS feature class
# Licensed library required: arcpy

import arcpy
import os
from config import SW_COND_TABLE, BUFFER_TYPE_TABLE, BUFFER_WIDTH_TABLE, \
    LANDUSE_DICT


class PLTS_Analysis(object):
    def __init__(self, GDB_PATH, FC_NAME):
        self.GBD_PATH = GDB_PATH
        self.FC_NAME = FC_NAME
        self.FC_PATH = os.path.join(self.GBD_PATH, self.FC_NAME)
        self.scoreFields = ["swCondScore",
                            "buffTypeScore",
                            "buffWidthScore",
                            "landuseScore",
                            "aggregateScore"]


    def _setupFields(self, inField, checklist):
        fc_fields = arcpy.ListFields(self.FC_PATH)
        fc_field_list = [field.name for field in fc_fields]

        for field in checklist:
            if field not in fc_field_list:
                raise NameError("{} is not found".format(field))

        if inField in fc_field_list:
            with arcpy.da.UpdateCursor(self.FC_PATH,
                                       inField) as cursor:
                for row in cursor:
                    row[0] = None
                    cursor.updateRow(row)

        else:
            arcpy.AddField_management(self.FC_PATH,
                                      inField,
                                      "SHORT")


    def assignSidewalkCondScore(self, sw_width = None, sw_cond = None):
        if not sw_cond or not sw_width:
            raise ValueError("Sidewalk Width and Sidewalk "
                                "Condition must be entered")
        self._setupFields(self.scoreFields[0], checklist=[sw_cond, sw_width])

        field_names = [sw_width, sw_cond, self.scoreFields[0]]
        with arcpy.da.UpdateCursor(self.FC_PATH, field_names) as cursor:
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

        del cursor, row


    def assignBufferTypeScore(self, buff_type = None, speed = None):
        if not speed or not buff_type:
            raise ValueError("Speed and Buffer Type must be entered")
        self._setupFields(self.scoreFields[1], checklist=[buff_type, speed])

        field_names = [buff_type, speed, self.scoreFields[1]]
        with arcpy.da.UpdateCursor(self.FC_PATH, field_names) as cursor:
            for row in cursor:
                # No Buffer
                if row[0] == "No Buffer":
                    if row[1] <= 25:
                        row[2] = BUFFER_TYPE_TABLE[0][0]
                    elif row[1] == 30:
                        row[2] = BUFFER_TYPE_TABLE[0][1]
                    elif row[1] == 35:
                        row[2] = BUFFER_TYPE_TABLE[0][2]
                    else:
                        row[2] = BUFFER_TYPE_TABLE[0][3]
                # Solid Surface
                elif row[1] == "Solid Surface":
                    if row[1] <= 25:
                        row[2] = BUFFER_TYPE_TABLE[1][0]
                    elif row[1] == 30:
                        row[2] = BUFFER_TYPE_TABLE[1][1]
                    elif row[1] == 35:
                        row[2] = BUFFER_TYPE_TABLE[1][2]
                    else:
                        row[2] = BUFFER_TYPE_TABLE[1][3]
                # Landscaped
                elif row[1] == "Landscaped":
                    if row[1] <= 25:
                        row[2] = BUFFER_TYPE_TABLE[2][0]
                    elif row[1] == 30:
                        row[2] = BUFFER_TYPE_TABLE[2][1]
                    elif row[1] == 35:
                        row[2] = BUFFER_TYPE_TABLE[2][2]
                    else:
                        row[2] = BUFFER_TYPE_TABLE[2][3]
                # Landscaped with tree or Vertical
                else:
                    if row[1] <= 25:
                        row[2] = BUFFER_TYPE_TABLE[3][0]
                    elif row[1] == 30:
                        row[2] = BUFFER_TYPE_TABLE[3][1]
                    elif row[1] == 35:
                        row[2] = BUFFER_TYPE_TABLE[3][2]
                    else:
                        row[2] = BUFFER_TYPE_TABLE[3][3]

                cursor.updateRow(row)

        del cursor, row


    def assignBufferWidthScore(self, buff_width = None, total_lanes = None):
        if not buff_width or not total_lanes:
            raise ValueError("Buffer Width and Total Lanes must be entered")
        self._setupFields(self.scoreFields[2], checklist=[buff_width,
                                                          total_lanes])

        field_names = [total_lanes, buff_width, self.scoreFields[2]]
        with arcpy.da.UpdateCursor(self.FC_PATH, field_names) as cursor:
            for row in cursor:
                # if offroad
                if row[0] is None:
                    row[2] = 1
                # Total 2 lanes
                elif row[0] == 2:
                    if row[1] < 5:
                        row[2] = BUFFER_WIDTH_TABLE[0][0]
                    elif row[1] >= 5 and row[1] < 10:
                        row[2] = BUFFER_WIDTH_TABLE[0][1]
                    elif row[1] >= 10 and row[1] < 15:
                        row[2] = BUFFER_WIDTH_TABLE[0][2]
                    elif row[1] >= 15 and row[1] < 25:
                        row[2] = BUFFER_WIDTH_TABLE[0][3]
                    else:
                        row[2] = BUFFER_WIDTH_TABLE[0][4]
                # 3 lanes
                elif row[0] == 3:
                    if row[1] < 5:
                        row[2] = BUFFER_WIDTH_TABLE[1][0]
                    elif row[1] >= 5 and row[1] < 10:
                        row[2] = BUFFER_WIDTH_TABLE[1][1]
                    elif row[1] >= 10 and row[1] < 15:
                        row[2] = BUFFER_WIDTH_TABLE[1][2]
                    elif row[1] >= 15 and row[1] < 25:
                        row[2] = BUFFER_WIDTH_TABLE[1][3]
                    else:
                        row[2] = BUFFER_WIDTH_TABLE[1][4]
                # 4-5 lanes
                elif row[0] == 4 or row[0] == 5:
                    if row[1] < 5:
                        row[2] = BUFFER_WIDTH_TABLE[2][0]
                    elif row[1] >= 5 and row[1] < 10:
                        row[2] = BUFFER_WIDTH_TABLE[2][1]
                    elif row[1] >= 10 and row[1] < 15:
                        row[2] = BUFFER_WIDTH_TABLE[2][2]
                    elif row[1] >= 15 and row[1] < 25:
                        row[2] = BUFFER_WIDTH_TABLE[2][3]
                    else:
                        row[2] = BUFFER_WIDTH_TABLE[2][4]
                # 6 lanes
                else:
                    if row[1] < 5:
                        row[2] = BUFFER_WIDTH_TABLE[3][0]
                    elif row[1] >= 5 and row[1] < 10:
                        row[2] = BUFFER_WIDTH_TABLE[3][1]
                    elif row[1] >= 10 and row[1] < 15:
                        row[2] = BUFFER_WIDTH_TABLE[3][2]
                    elif row[1] >= 15 and row[1] < 25:
                        row[2] = BUFFER_WIDTH_TABLE[3][3]
                    else:
                        row[2] = BUFFER_WIDTH_TABLE[3][4]

                cursor.updateRow(row)
        del cursor, row


    def assignLandUseScore(self, landUse = None):
        if not landUse:
            raise ValueError("Land use must be entered")
        self._setupFields(self.scoreFields[3], checklist=[landUse])

        fields_name = [landUse, self.scoreFields[3]]

        with arcpy.da.UpdateCursor(self.FC_PATH, fields_name) as cursor:
            for row in cursor:
                row[1] = LANDUSE_DICT["{}".format(row[0])]
                cursor.updateRow(row)

        del cursor, row


    def aggregateScore(self, method = "MAX"):
        self._setupFields(self.scoreFields[-1],
                          checklist=self.scoreFields[0:-1])
        with arcpy.da.UpdateCursor(self.FC_PATH, self.scoreFields) as cursor:
            for row in cursor:
                if method == "MAX":
                    row[-1] = max(row[:-1])
                elif method == "MIN":
                    row[-1] = min(row[:-1])
                cursor.updateRow(row)

        del cursor, row


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
    FC_NAME = "sidewalk_comp"

    convertScoreCategory(fc_path=os.path.join(GDB_PATH, FC_NAME),
                         inputField="ScoreCondition")

    plts = PLTS_Analysis(GDB_PATH, FC_NAME)
    plts.assignSidewalkCondScore(sw_cond = "CondScoreCat",
                              sw_width = "Width")
    plts.assignBufferTypeScore(buff_type="buffer_type",
                               speed="SPEED")
    plts.assignBufferWidthScore(buff_width="buffer_width",
                                total_lanes="totalLane")
    plts.assignLandUseScore(landUse="landuse")
    plts.aggregateScore()


if __name__ == "__main__":
    main()