# Class for PLTS assessment
from cuuats.snt.lts.lts_postgis import Lts
from cuuats.snt.lts.model.Segment import Segment
from cuuats.snt.lts.model.Approach import Approach
from cuuats.snt.lts.model.Sidewalk import Sidewalk
from cuuats.snt.lts import config as c


class Plts(Lts):
    def __init__(self, segment, sidewalks, approaches):
        if type(segment) is Segment:
            self.segment = segment
        else:
            raise TypeError('segment is not a Segment object')

        self.sidewalks = []
        for s in sidewalks:
            if type(s) is Sidewalk:
                self.sidewalks.append(s)
            else:
                raise TypeError('sidewalk is not a Sidewalk object')

        self.approaches = []
        for a in approaches:
            if type(a) is Approach:
                self.approaches.append(a)
            else:
                raise TypeError('approach is not an Approach object')

        self.plts_score = 0
        self.condition_score = 0
        self.physical_buffer_score = 0
        self.buffer_width_score = 0
        self.landuse_score = 0
        self.collector_crossing_score = 0
        self.arterial_crossing_score = 0
        self.total_lanes_crossed = 0

    def _calculate_condition_score(self):
        score = 0
        score = self._calculate_score(
            c.SW_COND_TABLE,
            ['self.sidewalk.sidewalk_width < 4',
             'self.sidewalk.sidewalk_width < 5',
             'self.sidewalk.sidewalk_width < 6',
             'True'],
            ['self.sidewalk.sidewalk_condition is "Good"',
             'self.sidewalk.sidewalk_condition is "Fair"',
             'self.sidewalk.sidewalk_condition is "Poor"',
             'True']
        )

        self.condition_score = max(self.condition_score, score)
        return(score)

    def _calculate_physical_buffer_score(self):
        score = 0
        score = self._calculate_score(
            c.BUFFER_TYPE_TABLE,
            ['self.sidewalk.buffer_type == "No Buffer"',
             'self.sidewalk.buffer_type == "Solid Buffer"',
             'self.sidewalk.buffer_type == "Landscaped"',
             'True'],
            ['self.segment.posted_speed <= 25',
             'self.segment.posted_speed == 30',
             'self.segment.posted_speed == 35',
             'True']
        )

        self.physical_buffer_score = max(self.physical_buffer_score, score)
        return(score)

    def _calculate_buffer_width_score(self):
        score = 0
        score = self._calculate_score(
            c.BUFFER_WIDTH_TABLE,
            ['self.segment.total_lanes <= 2',
             'self.segment.total_lanes == 3',
             'self.segment.total_lanes <= 5',
             'True'],
            ['self.sidewalk.buffer_width < 5',
             'self.sidewalk.buffer_width < 10',
             'self.sidewalk.buffer_width < 15',
             'self.sidewalk.buffer_width < 25',
             'True']
        )

        self.buffer_width_score = max(self.buffer_width_score, score)
        return(score)

    def _calculate_general_landuse(self):
        score = 0
        score = int(self.sidewalk.overall_landuse)
        # data structure for landuse is stored as the exact value
        # self.general_landuse_score = LANDUSE_DICT.get(self.general_landuse,
        #   0)
        self.sidewalk.landuse_score = max(self.sidewalk.landuse_score, score)
        return(score)

    def _calculate_collector_crossing_score(self):
        score = 0
        score = self._calculate_score(
            c.COLLECTOR_CROSSING_TABLE,
            ['self.segment.posted_speed <= 25',
             'self.segment.posted_speed == 30',
             'self.segment.posted_speed == 35',
             'True'],
            ['self.total_lanes_crossed <= 1',
             'True']
        )
        self.collector_crossing_score = max(self.collector_crossing_score,
                                            score)
        return(score)

    def _calculate_arterial_crossing_score(self):
        score = 0
        if self.total_lanes_crossed <= 2:
            score = self._calculate_score(
                c.ARTERIAL_CROSSING_TWO_LANES_TABLE,
                ['self.segment.posted_speed <= 25',
                 'self.segment.posted_speed == 30',
                 'self.segment.posted_speed == 35',
                 'True'],
                ['self.segment.aadt < 5000',
                 'self.segment.aadt < 9000',
                 'True']
            )
        else:
            score = self._calculate_score(
                c.ARTERIAL_CROSSING_THREE_LANES_TABLE,
                ['self.segment.posted_speed <= 25',
                 'self.segment.posted_speed == 30',
                 'self.segment.posted_speed == 35',
                 'True'],
                ['self.segment.aadt < 8000',
                 'self.segment.aadt < 12000',
                 'True']
            )
        self.arterial_crossing_score = max(self.arterial_crossing_score, score)
        return score

    def calculate_plts(self):
        # sidewalk criteria scores
        for sidewalk in self.sidewalks:
            self.sidewalk = sidewalk
            self._calculate_condition_score()
            self._calculate_physical_buffer_score()
            self._calculate_buffer_width_score()

        # crossing related scores
        for approach in self.approaches:
            self.approach = approach
            self._calculate_total_lanes_crossed()
            if self.segment.categorize_functional_class() == "C":
                self._calculate_collector_crossing_score()
            else:
                self._calculate_arterial_crossing_score()

        self.plts_score = self._aggregate_score(
            self.condition_score,
            self.physical_buffer_score,
            self.buffer_width_score,
            self.landuse_score,
            method="MAX"
        )


if __name__ == '__main__':
    # how to use the plts class
    sidewalks = [Sidewalk(sidewalk_width=15,
                          buffer_type='No Buffer',
                          buffer_width=0,
                          sidewalk_score=60),
                 Sidewalk(sidewalk_width=15,
                          buffer_type='Solid Buffer',
                          buffer_width=20,
                          sidewalk_score=80)]
    segment = Segment(posted_speed=30,
                      total_lanes=3,
                      functional_class=6,
                      marked_center_lane='Yes')
    approaches = [Approach(lane_configuration="XXT",
                           right_turn_lane_length=50,
                           right_turn_lane_config="Single",
                           bike_lane_approach="Straight"),
                  Approach(lane_configuration="XXT",
                           right_turn_lane_length=151,
                           right_turn_lane_config="Dual",
                           bike_lane_approach="Left")]

    plts = Plts(segment=segment, sidewalks=sidewalks, approaches=approaches)
    plts.calculate_plts()
    print(plts.plts_score)
