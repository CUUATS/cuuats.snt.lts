# Approach class for LTS
from .lanes import Lanes


class Approach(object):
    def __init__(self, **kwargs):
        self.lanes = Lanes(kwargs.get('lane_configuration'))
        self.right_turn_lane_length = kwargs.get('right_turn_lane_length') or 0
        self.right_turn_lane_config = kwargs.get('right_turn_lane_config')
        self.bike_lane_approach = kwargs.get('bike_lane_approach')
        self.median_present = kwargs.get('median_present')
        self.control_type = kwargs.get('control_type')

    def is_signalized(self):
        if self.control_type == 'signalized':
            return True
        else:
            return False
