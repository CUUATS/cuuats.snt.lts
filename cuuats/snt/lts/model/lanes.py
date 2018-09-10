class Lanes:
    def __init__(self, config):
        self.config = config

    def __len__(self):
        if self.config is None:
            return 0
        return len(self.config)

    @property
    def max_lane(self):
        """
        this function takes lane configuration string and return the max lane
        in either direction
        :param self: self
        :param lane_config: coded string of lane configuration
        :return: int represent max lane
        """
        if self.config is None:
            max_lane = 1
        else:
            away_lane = len(self.config[self.config.find("X"):
                            self.config.rfind("X")+1])
            incomeing_lane = len(self.config[self.config.rfind("X")+1:])
            max_lane = max(away_lane, incomeing_lane)

        return(max_lane)

    @property
    def lanes_crossed(self):
        """
        this function takes lane configuration string and return the
        lanecrossed from righter most lane to the left turn lane
        :param self: self
        :param lane_config: coded string of lane_config
        :return:
        """
        if self.config in [None, 'X', 'XX', 'XXX']:
            lanecrossed = 0
        else:
            lanecrossed = len(self.config) - self.config.rfind("X") - 2
        return(lanecrossed)
