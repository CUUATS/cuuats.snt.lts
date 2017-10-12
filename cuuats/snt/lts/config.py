# Path Variables:
# SDE_DB = r"G:\Resources\Connections\PCD_Edit_aadt.sde"
# STREET_NAME = "PCD.PCDQC.StreetIntersectionApproach"

SDE_DB = r"G:\Resources\Connections\PCD_Edit_aadt.sde"
APPROACH_NAME = "PCD.PCDQC.StreetIntersectionApproach"
SEGMENT_NAME = "PCD.PCDQC.StreetSegment"
SIDEWALK_NAME = "PCD.PCDQC.SidewalkSegment"
REL_NAME = "PCD.PCDQC.SidewalkSegment_StreetSegment"

# BLTS - SEGMENT SCORING TABLE
## Bike Lane with Adjacent Parking Lane Criteria Scorintg Table
BL_ADJ_PK_TABLE = [[1, 2, 3, 2, 3],
                   [1, 2, 3, 2, 3],
                   [2, 3, 3, 3, 3],
                   [2, 4, 4, 3, 4]]


## Bike Lane without Adjacent Parking Lane Criteria Scoring Table
BL_NO_ADJ_PK_TABLE = [[1, 1, 2, 3, 1, 3],
                      [2, 3, 3, 3, 2, 3],
                      [3, 4, 4, 4, 3, 4]]


## Urban/Suburban Mixed Traffic Criteria Scoring Table
MIXED_TRAF_TABLE = [[1, 2, 3, 4],
                    [2, 3, 4, 4],
                    [3, 4, 4, 4]]


## Right Turn Lane Criteria Scoring Table
RTL_CRIT_TABLE = [2, 3, 3, 4]


## Left Turn Lane Criteria Scoring Table
LTL_CRIT_TABLE = [[2, 2, 3, 4],
                  [2, 3, 4, 4],
                  [3, 4, 4, 4]]

## Unsignalized Intersection Crossing Without a Median Refuge Criteria
## Scoring Table
CROSS_NO_MED_TABLE = [[1, 2, 4],
                      [1, 2, 4],
                      [2, 3, 4],
                      [3, 4, 4]]


## Unsignalized Intersection Crossing With a Median Refuge Criteria
## Scoring Table
CROSS_HAS_MED_TABLE = [[1, 1, 2],
                       [1, 2, 3],
                       [2, 3, 4],
                       [3, 4, 4]]


# PLTS - SIDEWALK SCORING TABLE
## Scoring table for Sidewalk Condition
SW_COND_TABLE = [[4, 4, 4, 4, 4],
                 [3, 3, 3, 4, 4],
                 [2, 2, 3, 4, 4],
                 [1, 1, 2, 3, 4]]


## Physical Buffer Type
BUFFER_TYPE_TABLE = [[2, 3, 3, 4],
                     [2, 2, 2, 2],
                     [1, 2, 2, 2],
                     [1, 1, 1, 2]]


## Total Buffer Width
BUFFER_WIDTH_TABLE = [[2, 2, 1, 1, 1],
                      [3, 2, 2, 1, 1],
                      [4, 3, 2, 1, 1],
                      [4, 4, 3, 2, 2]]


## Land Use
LANDUSE_DICT = {"residential": 1,
                "CBD": 1,
                "neighborhood commericial": 1,
                "parks and other facilities": 1,
                "governmental buildings": 1,
                "plaza": 1,
                "office parks": 1,
                "low density development": 2,
                "rural subdivision": 2,
                "un-incorporated communities": 2,
                "strip commerical": 2,
                "mixed employment": 2,
                "light industrial": 3,
                "big-box": 3,
                "heavy industry": 4,
                "intermodal facilities": 4,
                "freeway interchages": 4}
