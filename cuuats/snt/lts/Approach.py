## Approach class for LTS

class Approach(object):
    def __init__(self, **kwargs):
        self.lane_configuration = kwargs.get('lane_configuration')
        self.right_turn_lane_length = kwargs.get('right_turn_lane_length')
        self.right_turn_lane_config = kwargs.get('right_turn_lane_config')
        self.bike_lane_approach = kwargs.get('bike_lane_approach')
