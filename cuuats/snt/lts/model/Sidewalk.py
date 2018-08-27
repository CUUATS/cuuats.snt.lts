# Sidewalk class for Lts`


class Sidewalk(object):
    def __init__(self, **kwargs):
        self.sidewalk_width = kwargs.get('sidewalk_width')
        self.buffer_type = kwargs.get('buffer_type')
        self.buffer_width = kwargs.get('buffer_width')
        self.sidewalk_score = kwargs.get('sidewalk_score')
        self.overall_landuse = kwargs.get('overall_landuse')

    def _convert_score_to_condition(self, score):
        if score > 70:
            score = 'Good'
        elif score > 60:
            score = 'Fair'
        elif score > 50:
            score = 'Poor'
        else:
            score = 'Very Poor'
        return(score)
