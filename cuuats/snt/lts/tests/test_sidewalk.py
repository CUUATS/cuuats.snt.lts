import unittest
from cuuats.snt.lts import Sidewalk


class TestSidewalk(unittest.TestCase):
    def test_convert_buffer_type(self):
        sidewalk = Sidewalk()
        self.assertEqual(sidewalk._convert_buffer_type(None), 'no buffer')
        self.assertEqual(sidewalk._convert_buffer_type(''), 'no buffer')
        self.assertEqual(sidewalk._convert_buffer_type('a'), 'a')


if __name__ == '__main__':
    unittest.main()
