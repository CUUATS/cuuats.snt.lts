# Sidewalk class for Lts`


class Sidewalk(object):
    def __init__(self, **kwargs):
        self.sidewalk_width = kwargs.get('sidewalk_width')
        self.buffer_type = self._convert_buffer_type(kwargs.get('buffer_type'))
        self.buffer_width = kwargs.get('buffer_width') or 0
        self.sidewalk_score = kwargs.get('sidewalk_score')
        self.overall_landuse = kwargs.get('overall_landuse')

    def _convert_buffer_type(self, buffer_type):
        if buffer_type == '':
            buffer_type = 'no buffer'
        elif buffer_type is None:
            buffer_type = 'no buffer'
        return buffer_type
