# crossing object for lts


class Crossing:
    def __init__(self, **kwargs):
        self.crossing_speed = kwargs.get('crossing_speed')
        self.control_type = kwargs.get('control_type')
        self.lanes = kwargs.get('lanes')
        self.median = kwargs.get('median') or None
