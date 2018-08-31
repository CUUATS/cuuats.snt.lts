# Approach class for LTS
from cuuats.snt.lts.lts_postgis import Lts


class Approach(object):
    def __init__(self, **kwargs):
        self.lane_configuration = kwargs.get('lane_configuration')
        self.right_turn_lane_length = Lts.remove_none(
                                        kwargs.get('right_turn_lane_length'))
        self.right_turn_lane_config = kwargs.get('right_turn_lane_config')
        self.bike_lane_approach = kwargs.get('bike_lane_approach')
        self.lanes_crossed = self._calculate_lanes_crossed(
                                    self.lane_configuration)
        self.max_lane = self._calculate_max_lane(self.lane_configuration)
        if self.lane_configuration is not None:
            self.total_lanes = len(self.lane_configuration)
        self.median_present = kwargs.get('median_present')
        self.control_type = kwargs.get('control_type')

    def _calculate_max_lane(self, lane_config):
        """
        this function takes lane configuration string and return the max lane
        in either direction
        :param self: self
        :param lane_config: coded string of lane configuration
        :return: int represent max lane
        """
        if lane_config is None:
            max_lane = 1
        else:
            away_lane = len(lane_config[lane_config.find("X"):
                            lane_config.rfind("X")+1])
            incomeing_lane = len(lane_config[lane_config.rfind("X")+1:])
            max_lane = max(away_lane, incomeing_lane)

        return(max_lane)

    def _calculate_lanes_crossed(self, lane_config):
        """
        this function takes lane configuration string and return the
        lanecrossed from righter most lane to the left turn lane
        :param self: self
        :param lane_config: coded string of lane_config
        :return:
        """
        if lane_config is None:
            lanecrossed = 0
        elif lane_config == "X" or lane_config == "XX" or lane_config == "XXX":
            lanecrossed = 0
        else:
            lanecrossed = len(lane_config) - \
                          lane_config.rfind("X") - 2
        return(lanecrossed)

    def is_signalized(self):
        if self.control_type == 'signalized':
            return True
        else:
            return False
