# force python 3.* compability
from __future__ import absolute_import, division, print_function
# regular imaports below:
import unittest
from rikedom_algorithms import hp_filter
from datetime import datetime
import logging
#logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

class MyTestCase(unittest.TestCase):
    def test_simulation(self):
        today = datetime.today().date()
        hp_filter.run_algorithm('NCC-A.ST', datetime(2014, 6, 2), datetime(today.year, today.month, today.day))


if __name__ == '__main__':
    unittest.main()

