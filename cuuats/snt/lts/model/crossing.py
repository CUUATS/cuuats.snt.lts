# crossing object for lts


class Crossing:
    def __init__(self, **kwargs):
        self.crossing_speed = kwargs.get('crossing_speed') or 0
        self.control_type = kwargs.get('control_type') or None
        self.lanes = kwargs.get('lanes') or 0
        self.median = kwargs.get('median') or None
