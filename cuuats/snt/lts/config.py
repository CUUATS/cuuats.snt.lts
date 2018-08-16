import pandas as pd

# BLTS - SEGMENT SCORING TABLE
# Bike Lane with Adjacent Parking Lane Criteria Scorintg Table
BL_ADJ_PK_TABLE_ONE_LANE = [[3, 2, 1],
                            [3, 2, 1],
                            [3, 3, 2],
                            [4, 4, 2]]
BL_ADJ_PK_AADT_SCALE = pd.IntervalIndex.from_arrays(
                    [-float('Inf'), 1000, 3000, 30000],
                    [1000, 3000, 30000, float('Inf')])
BL_ADJ_PK_WIDTH_SCALE = pd.IntervalIndex.from_arrays(
                    [-float('Inf'), 13, 14.5],
                    [13, 14.5, float('Inf')])


BL_ADJ_PK_TABLE_TWO_LANES = [[3, 2],
                             [3, 2],
                             [3, 3],
                             [4, 3]]
BL_ADJ_PK_TWO_WIDTH_SCALE = pd.IntervalIndex.from_arrays(
                    [-float('Inf'), 14.5],
                    [14.5, float('Inf')])

# Bike Lane without Adjacent Parking Lane Criteria Scoring Table
BL_NO_ADJ_PK_TABLE_ONE_LANE = [[1, 1, 2],
                               [2, 3, 3],
                               [3, 4, 4]]

BL_NO_ADJ_PK_TABLE_TWO_LANES = [[1, 3],
                                [2, 3],
                                [3, 4]]

# Urban/Suburban Mixed Traffic Criteria Scoring Table
MIXED_TRAF_TABLE = [[1, 2, 3, 4],
                    [2, 3, 4, 4],
                    [3, 4, 4, 4]]
# Scale for Mix Traffic
URBAN_FIX_TRAFFIC_AADT_SCALE = pd.IntervalIndex.from_arrays(
                    [-float('Inf'), 3000, 30000],
                    [3000, 30000, float('Inf')])
URBAN_FIX_TRAFFIC_LANE_SCALE = pd.IntervalIndex.from_arrays(
                    [-float('Inf'), 0, 1, 2],
                    [0, 1, 2, float('Inf')])

# Right Turn Lane Criteria Scoring Table
RTL_CRIT_TABLE = [2, 3, 3, 4]


# Left Turn Lane Criteria Scoring Table
LTL_DUAL_SHARED_TABLE = [4, 4, 4]

LTL_CRIT_TABLE = [[2, 2, 3],
                  [2, 3, 4],
                  [3, 4, 4]]

# Unsignalized Intersection Crossing Without a Median Refuge Criteria
# Scoring Table
CROSSING_NO_MED_TABLE = [[1, 2, 4],
                         [1, 2, 4],
                         [2, 3, 4],
                         [3, 4, 4]]


# Unsignalized Intersection Crossing With a Median Refuge Criteria
# Scoring Table
CROSSING_HAS_MED_TABLE = [[1, 1, 2],
                          [1, 2, 3],
                          [2, 3, 4],
                          [3, 4, 4]]


# PLTS - SIDEWALK SCORING TABLE
# Scoring table for Sidewalk Condition
SW_COND_TABLE = [[4, 4, 4, 4],
                 [3, 3, 3, 4],
                 [2, 2, 3, 4],
                 [1, 1, 2, 3]]


# Physical Buffer Type
BUFFER_TYPE_TABLE = [[2, 3, 3, 4],
                     [2, 2, 2, 2],
                     [1, 2, 2, 2],
                     [1, 1, 1, 2]]


# Total Buffer Width
BUFFER_WIDTH_TABLE = [[2, 2, 1, 1, 1],
                      [3, 2, 2, 1, 1],
                      [4, 3, 2, 1, 1],
                      [4, 4, 3, 2, 2]]

# Collector and local unsignalized intersection crossing
COLLECTOR_CROSSING_TABLE = [[1, 1],
                            [1, 2],
                            [2, 2],
                            [3, 3]]

# Arterial unsignalized intersection crossing - 2 lanes
ARTERIAL_CROSSING_TWO_LANES_TABLE = [[2, 2, 3],
                               [2, 3, 3],
                               [3, 3, 4],
                               [3, 4, 4]]

# Arterial unsignalized intersection crossing - 3 lanes
ARTERIAL_CROSSING_THREE_LANES_TABLE = [[3, 3, 4],
                               [3, 3, 4],
                               [3, 4, 4],
                               [4, 4, 4]]

# Land Use
LANDUSE_DICT = {"residential": 1,
                "CBD": 1,
                "neighborhood commercial": 1,
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
