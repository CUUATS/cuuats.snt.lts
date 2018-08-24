# Unit Test for Segment Class
import unittest
from cuuats.snt.lts.model.Segment import Segment


class SegmentTest(unittest.TestCase):
    def test_categorize_functional_class(self):
        segment = Segment()
        segment.functional_class = None
        self.assertEqual(segment._categorize_functional_class(), 'C')
        segment.functional_class = 4
        self.assertEqual(segment._categorize_functional_class(), 'C')
        segment.functional_class = 1
        self.assertEqual(segment._categorize_functional_class(), 'A')

    def test_calculate_mix_traffic(self):

if __name__ == '__main__':
    unittest.main()
