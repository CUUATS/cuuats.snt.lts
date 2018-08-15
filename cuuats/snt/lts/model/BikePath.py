# BikePath Class for LTS


class BikePath(object):
    def __init__(self, **kwargs):
        self.path_type = kwargs.get('path_type')
        self.path_subtype = kwargs.get('path_subtype')
        self.path_category = kwargs.get('path_category')
        self.width = kwargs.get('width')
        self.buffer_width = kwargs.get('buffer_wdith')
        self.buffer_type = kwargs.get('buffer_type')
