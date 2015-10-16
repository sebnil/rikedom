# force python 3.* compability
from __future__ import absolute_import, division, print_function
# regular imaports below:
import unittest
from rikedom_algorithms.hp_filter import HodrickPrescottAlgorithm
from datetime import datetime
import logging
#logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

class MyTestCase(unittest.TestCase):
    def test_simulation(self):
        today = datetime.today().date()
        hp_algo = HodrickPrescottAlgorithm()

        cherrypick_portfolio = [
            #'SKF-B.ST', # SKF. industry. beta 1.12
            'AZN.ST', # astra zeneca. medicine
            'VOLV-B.ST', # Volvo. industry. beta 1.54
            'AXFO.ST', # axfood. food. beta 0.48
            #'INVE-B.ST', # investor. property and finance. beta 1.03,
            'SAND.ST', # sandvik. industry. beta 1.21,
            'AAK.ST', # food. 0.63,
            'ALFA.ST', # alfa laval. industry. 1.0
            'ASSAB.ST', # assa abloy (locks). industry. beta 0.89
            'NCC-A.ST', # NCC. construction. 1.22
            'WALL-B.ST', # wallenstam. property. 0.63,
            'STL.OL', #statoil. norwegian. 1,08
            #'^OMX', # stockholm index
            #'BSE-100.BO', # india index.
        ]

        #hp_algo.run_algorithm(['NCC-A.ST'], datetime(2014, 6, 2), datetime(today.year, today.month, today.day))
        hp_algo.run_algorithm(cherrypick_portfolio, datetime(2014, 6, 2), datetime(today.year, today.month, today.day))


if __name__ == '__main__':
    unittest.main()

