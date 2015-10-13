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
import logging
logging.basicConfig(level=logging.DEBUG)

def init

def perform_simulation(data):
    for simulated_date in data.index:
        step(data, simulated_date)

def step(data, simulated_date, function=None):
    data_available_until = simulated_date - Timedelta('1 days')
    available_data = data[:data_available_until]

    function(data, simulated_date)

