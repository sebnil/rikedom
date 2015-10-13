# force python 3.* compability
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
# regular imaports below:
import sys
sys.path.append('../../zipline-test/') # add parent directory to path
from helpers.security_loader import load_from_yahoo
from pandas import Timedelta
from datetime import datetime
from rikedom import simulator
import logging
logging.basicConfig(level=logging.DEBUG)

def step(available_data, simulated_date):
    pass

def run_algorithm(security='AAPL', start=datetime(2014, 1, 1), end=datetime.now() ):
    logging.debug('run_algorithm begin {}'.format(locals()))

    # get data from yahoo
    data = load_from_yahoo(stocks=[security], indexes={}, start=start, end=end)
    logging.debug('done loading from yahoo. {} {} {}'.format(security, start, end))

    logging.debug('starting to run algo...')
    simulator.perform_simulation(data)
    logging.debug('done running algo')
