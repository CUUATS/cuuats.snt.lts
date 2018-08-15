# Segment Class for LTS Assessment


class Segment(object):
    def __init__(self, **kwargs):
        self.bicycle_facility_type = kwargs.get('bicycle_facility_type')
        self.bicycle_facility_width = kwargs.get('bicycle_facility_width')
        self.lanes_per_direction = kwargs.get('lanes_per_direction')
        self.parking_lane_width = kwargs.get('parking_lane_width')
        self.aadt = int(self._remove_none(kwargs.get('aadt')))
        self.functional_class = kwargs.get('functional_class')
        self.posted_speed = kwargs.get('posted_speed')
        self.total_lanes = kwargs.get('total_lanes')
        self.marked_center_lane = kwargs.get('marked_center_lane')

    def _remove_none(self, value):
        if value is None:
            value = 0
        return value

    def categorize_functional_class(self):
        if self.functional_class is None:
            return "C"
        if self.functional_class >= 4:
            return "C"
        else:
            return "A"
