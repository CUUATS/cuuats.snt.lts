import arcpy
import os
import shutil
import tempfile
import blts_arcpy as blts


class workSpaceFixture(object):
    GDB_NAME = 'Temp.gdb'
    FC_NAME = 'StreetCL'
    FC_TYPE = 'POLYLINE'
    FC_FIELD = (
        ('roadName', 'TEXT', 50),
        ('speed', 'LONG', 5),
        ('lpd', 'LONG', 5),
        ('combParkingWidth', 'LONG', 5),
        ('hasParkingLane', 'LONG', 5),
        ('width', 'LONG', 5),
        ('RTL_Conf_N', 'LONG', 5),
        ('RTL_Conf_S', 'LONG', 5),
        ('RTL_Conf_E', 'LONG', 5),
        ('RTL_Conf_W', 'LONG', 5),
        ('RTL_Len_N', 'LONG', 5),
        ('RTL_Len_S', 'LONG', 5),
        ('RTL_Len_E', 'LONG', 5),
        ('RTL_Len_W', 'LONG', 5),
        ('bike_AA_N', 'LONG', 5),
        ('bike_AA_S', 'LONG', 5),
        ('bike_AA_E', 'LONG', 5),
        ('bike_AA_W', 'SHORT', 5),
        ('LTL_Conf_N', 'LONG', 5),
        ('LTL_Conf_S', 'LONG', 5),
        ('LTL_Conf_E', 'LONG', 5),
        ('LTL_Conf_W', 'LONG', 5),
        ('LTL_lanescrossed_N', 'LONG', 5),
        ('LTL_lanescrossed_S', 'LONG', 5),
        ('LTL_lanescrossed_E', 'LONG', 5),
        ('LTL_lanescrossed_W', 'LONG', 5),
        ('med_present', 'TEXT', 10),
        ('TotalLanes_EW1', 'LONG', 5),
        ('TotalLanes_NS', 'LONG', 5),
        ('Control_Type', 'TEXT', 10),
        ('thruLane_EW', 'LONG', 5),
        ('thruLane_NS', 'LONG', 5)
    )


    @classmethod
    def setUpModule(cls):
        # Create the paths
        cls.workspace_dir = tempfile.mkdtemp()
        print(cls.workspace_dir)
        cls.GDB_Path = os.path.join(cls.workspace_dir, cls.GDB_NAME)
        cls.FC_Path = os.path.join(cls.GDB_Path, cls.FC_NAME)


        # Create a file geodatabase
        arcpy.CreateFileGDB_management(cls.workspace_dir, cls.GDB_NAME)

        # Create feature class
        arcpy.CreateFeatureclass_management(
            cls.GDB_Path, cls.FC_NAME, cls.FC_TYPE
        )

        # Add field to the feature class
        for (field_name, field_type, field_precision) in cls.FC_FIELD:
            arcpy.AddField_management(
                cls.FC_Path, field_name, field_type, field_precision
            )

    @classmethod
    def tearDownModule(cls):
        shutil.rmtree(cls.workspace_dir)
        print("Complete tearing down")



class testingModule(object):
    @classmethod
    def _addData(cls, field, data):
    # Add data to the field
        fields_name = [f for f in field]
        with arcpy.da.InsertCursor(workSpaceFixture.FC_Path,
                                   fields_name) as cursor:
            for row in data:
                cursor.insertRow(row)

        del cursor, row


    @classmethod
    def _deleteData(self):
        arcpy.DeleteRows_management(workSpaceFixture.FC_Path)


    @classmethod
    def mixTrafficVerify(cls):
        data = []
        field = ('speed', 'lpd')
        speed = [20, 25, 30, 35, 40]
        lpd = [0, 1, 2, 3, 4]
        expected_score = [1,2,3,4,4,
                          1,2,3,4,4,
                          2,3,4,4,4,
                          3,4,4,4,4,
                          3,4,4,4,4]

        # add test data
        for s in speed:
            for l in lpd:
                data.append((s,l))

        cls._addData(field, data)

        a = blts.BLTS_Analysis(workSpaceFixture.GDB_Path,
                               workSpaceFixture.FC_NAME)
        a.addField()
        a.setMixTrafficField('speed', 'lpd')
        a.assignMixTrafficScore()

        cursor = arcpy.SearchCursor(workSpaceFixture.FC_Path)
        calScore = []
        for row in cursor:
            calScore.append(row.getValue("mixTraffic"))


        if calScore == expected_score:
            print("All Mix Traffic score is as expected...")
        else:
            print("Calculated score and expected mix traffic score does not match")

        cls._deleteData()
        del cursor, row, a


    @classmethod
    def bikeLaneWithPkVerify(cls):
        data = []
        field = ('hasParkingLane', 'lpd', 'speed', 'combParkingWidth')
        hasParking = [50, 100]
        lpd = [0, 1, 2, 3]
        speed = [20, 25, 30, 35, 40, 45]
        combParkingWidth = [16, 15, 14, 13, 12]
        expected_score = [1, 1, 2, 3, 3,
                          1, 1, 2, 3, 3,
                          1, 1, 2, 3, 3,
                          2, 2, 3, 3, 3,
                          2, 2, 4, 4, 4,
                          2, 2, 4, 4, 4,] * 2 + \
                         [2, 2, 3, 3, 3,
                          2, 2, 3, 3, 3,
                          2, 2, 3, 3, 3,
                          3, 3, 3, 3, 3,
                          3, 3, 4, 4, 4,
                          3, 3, 4, 4, 4] * 2 + \
                         [None] * 6 * 5 * 2 * 2

        for h in hasParking:
            for l in lpd:
                for s in speed:
                    for c in combParkingWidth:
                        data.append((h,l,s,c))

        cls._addData(field, data)
        a = blts.BLTS_Analysis(workSpaceFixture.GDB_Path,
                               workSpaceFixture.FC_NAME)
        a.setPkLaneField("lpd", "speed", "combParkingWidth", "HasParkingLane")
        a.assignBLwithPkLane()

        cursor = arcpy.SearchCursor(workSpaceFixture.FC_Path)
        calScore = []
        for row in cursor:
            calScore.append(row.getValue("pkLane"))

        if calScore == expected_score:
            print("All Bike Lane with Adj Parking score is as expected...")
        else:
            print("Calculated score and BL w/ parking score does not match")

        cls._deleteData()
        del a, cursor, row


    @classmethod
    def bikeLaneWithoutPkVerify(cls):
        data = []
        field = ('hasParkingLane', 'lpd', 'speed', 'width')
        hasParking = [50, 100]
        lpd = [0, 1, 2, 3]
        speed = [25, 30, 35, 40, 45]
        width = [8, 7, 6, 5]
        expected_score = [None] * 80 + \
                         [1, 1, 1, 2,
                          1, 1, 1, 2,
                          2, 2, 3, 3,
                          3, 3, 4, 4,
                          3, 3, 4, 4,] * 2 + \
                          [1, 1, 3, 3,
                           1, 1, 3, 3,
                           2, 2, 3, 3,
                           3, 3, 4, 4,
                           3, 3, 4, 4] * 2

        for h in hasParking:
            for l in lpd:
                for s in speed:
                    for c in width:
                        data.append((h,l,s,c))

        cls._addData(field, data)
        a = blts.BLTS_Analysis(workSpaceFixture.GDB_Path,
                               workSpaceFixture.FC_NAME)
        a.setNoPkLaneField("lpd", "speed", "width", "HasParkingLane")
        a.assignBLwithoutPkLane()

        cursor = arcpy.SearchCursor(workSpaceFixture.FC_Path)
        calScore = []
        for row in cursor:
            calScore.append(row.getValue("noPkLane"))

        if calScore == expected_score:
            print("All Bike Lane w/o Adj Parking score is as expected...")
        else:
            print("Calculated score and BL w/o parking score does not match")

        cls._deleteData()
        del a, cursor, row


def main():
        workSpaceFixture.setUpModule()
        testingModule.mixTrafficVerify()
        testingModule.bikeLaneWithPkVerify()
        testingModule.bikeLaneWithoutPkVerify()
        #workSpaceFixture.tearDownModule()


if __name__ == ("__main__"):
    main()










