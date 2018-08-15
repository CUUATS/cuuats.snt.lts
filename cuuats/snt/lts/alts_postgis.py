# Alts class for Lts

from cuuats.snt.lts.lts_postgis import Lts
from cuuats.snt.lts.model.Segment import Segment
# from cuuats.snt.lts.model.Approach import Approach
# from cuuats.snt.lts import config as c


class Alts(Lts):
    def __init__(self, segment):
        if type(segment) is Segment:
            self.segment = segment
        else:
            raise TypeError('segment is not an Segment object')

    def _calcualate_functional_class(self):
        pass

    def calculate_alts(self):
        pass


if __name__ == '__main__':
    alts = Alts(segment=Segment())
