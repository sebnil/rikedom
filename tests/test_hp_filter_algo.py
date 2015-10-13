# force python 3.* compability
from __future__ import absolute_import, division, print_function
# regular imaports below:
import unittest
from rikedom_algorithms import hp_filter
from datetime import datetime

class MyTestCase(unittest.TestCase):
    def test_simulation(self):
        hp_filter.run_algorithm('NCC-A.ST', datetime(2014, 1, 1), datetime.now())


if __name__ == '__main__':
    unittest.main()
