# Class for PLTS assessment
from cuuats.snt.lts.lts_postgis import Lts
from cuuats.snt.lts.model.Segment import Segment
from cuuats.snt.lts.model.Approach import Approach
from cuuats.snt.lts.model.Sidewalk import Sidewalk
from cuuats.snt.lts import config as c

class Plts(Lts):
    def __init__(self, **kwargs):
        self.sidewalk = kwargs.get('sidewalk')
        self.segment = kwargs.get('segment')

        self.plts_score = 0
        self.condition_score = 0
        self.physical_buffer_score = 0
        self.buffer_width_score = 0
        self.land_use_score = 0

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

    def _calculate_physical_buffer(self):
        score = 0
        score = self._calcuate_score(
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

    def calculate_plts(self):
        self._calculate_condition_score()

        self.plts_score = self._aggregate_score(
            self.condition_score,
            self.physical_buffer_score,
            method = "MAX"
        )

if __name__ == '__main__':
    sidewalk = Sidewalk(sidewalk_width = 15,
                        buffer_type = 'No Buffer',
                        buffer_width = 0,
                        sidewalk_score = 60)
    segment = Segment(posted_speed = 30)
    plts = Plts(sidewalk = sidewalk, segment = segment)
    plts.calculate_plts()
    import pdb; pdb.set_trace()
