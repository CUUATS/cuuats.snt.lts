import unittest
from .test_segment import TestSegment
from .test_sidewalk import TestSidewalk


def test_suite():
    return unittest.TestSuite([
        TestSegment(),
        TestSidewalk(),
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
