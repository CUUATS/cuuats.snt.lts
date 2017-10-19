import unittest
import arcpy
import gc
import os
import shutil
import tempfile
import unittest
from cuuats.datamodel.exceptions import ObjectDoesNotExist, \
    MultipleObjectsReturned
from cuuats.datamodel.workspaces import Workspace
from cuuats.datamodel.fields import BaseField, OIDField, GeometryField, \
    StringField, NumericField, ScaleField, MethodField, WeightsField
from cuuats.datamodel.manytomany import ManyToManyField
from cuuats.datamodel.features import BaseFeature
from cuuats.datamodel.scales import BreaksScale, DictScale
from cuuats.datamodel.domains import CodedValue, D
from cuuats.datamodel.workspaces import WorkspaceManager
from blts_cuuats import calculate_score, calculate_mix_traffic, \
    calculate_bikelane_with_adj_parking


class TestBLTS(unittest.TestCase):
    PostedSpeed = 50
    BikeLaneWidth = 10
    IDOTAADT = 500
    LanesPerDirection = None

    def test_data_setup(self):
        self.assertEqual(self.IDOTAADT, 500)
        self.assertTrue(self.LanesPerDirection is None)
        self.TestData = 500
        self.assertEqual(self.TestData, 500)

    def test_calculate_score(self):
        # Test calculate score function
        IDOTAADT = [500, 1500, 3500]
        LanesPerDirection = [0, 1, 2, 3]
        score_matrix = [[1, 2, 3, 4],
                        [2, 3, 4, 4],
                        [3, 4, 4, 4]]
        outer_list = []
        inner_list = []
        for i in IDOTAADT:
            self.IDOTAADT = i
            for l in LanesPerDirection:
                self.LanesPerDirection = l
                score = calculate_score(
                    self,
                    score_matrix,
                    ['self.IDOTAADT <= 1000',
                     'self.IDOTAADT <= 3000',
                     'True'],
                    ['self.LanesPerDirection in (0, None)',
                     'self.LanesPerDirection == 1',
                     'self.LanesPerDirection == 2',
                     'self.LanesPerDirection >= 3'])
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_mix_traffic(self):
        # Test the mix traffic function
        IDOTAADT = [500, 1500, 3500]
        LanesPerDirection = [0, 1, 2, 3]
        score_matrix = [[1, 2, 3, 4],
                        [2, 3, 4, 4],
                        [3, 4, 4, 4]]
        outer_list = []
        inner_list = []
        for i in IDOTAADT:
            self.IDOTAADT = i
            for l in LanesPerDirection:
                self.LanesPerDirection = l
                score = calculate_mix_traffic(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

    def test_bikelane_with_adj_parking(self):
        # Test Bike Facility and Parking Lane Width Filter
        self.BicycleFacilityWidth = None
        self.ParkingLaneWidth = None
        self.assertEqual(calculate_bikelane_with_adj_parking(self), 99)
        self.BicycleFacilityWidth = 1
        self.assertEqual(calculate_bikelane_with_adj_parking(self), 99)

        # Test 1 Lane Per Direction
        self.LanesPerDirection = 1
        IDOTAADT = [None, 1500, 3500, 50000]
        BicycleFacility = [10, 7, 4]
        ParkingLaneWidth = [6, 7, 4]
        score_matrix = [[1, 2, 3],
                        [1, 2, 3],
                        [2, 3, 3],
                        [2, 4, 4]]
        outer_list = []
        inner_list = []
        for i in IDOTAADT:
            self.IDOTAADT = i
            for (b, p) in zip(BicycleFacility, ParkingLaneWidth):
                self.BicycleFacilityWidth = b
                self.ParkingLaneWidth = p
                score = calculate_bikelane_with_adj_parking(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)

        # Test 2 Lane Per Direction
        self.LanesPerDirection = 2
        IDOTAADT = [500, 3000, 30000, 30001]
        BicycleFacility = [10, 7]
        ParkingLaneWidth = [5, 7]
        score_matrix = [[2, 3],
                        [2, 3],
                        [3, 3],
                        [3, 4]]
        outer_list = []
        inner_list = []
        for i in IDOTAADT:
            self.IDOTAADT = i
            for (b, p) in zip(BicycleFacility, ParkingLaneWidth):
                self.BicycleFacilityWidth = b
                self.ParkingLaneWidth = p
                score = calculate_bikelane_with_adj_parking(self)
                inner_list.append(score)
            outer_list.append(inner_list)
            inner_list = []

        self.assertEqual(outer_list, score_matrix)






















if __name__ == '__main__':
    unittest.main()
