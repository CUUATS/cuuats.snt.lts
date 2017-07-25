import arcpy
import os
import shutil
import tempfile

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


    @classmethod
    def addData(cls):
    # Add data to the field
        fields_name = [f[0] for f in cls.FC_FIELD]
        with arcpy.da.InsertCursor(cls.FC_Path, fields_name) as cursor:
            for row in cls.FC_DATA:
                cursor.insertRow(row)



def main():
    try:
        workSpaceFixture.setUpModule()
    finally:
        pass
        #workSpaceFixture.tearDownModule()


if __name__ == ("__main__"):
    main()










