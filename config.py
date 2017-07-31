# SIDEWALK SCORING TABLE
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