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

class TradingSimulator:
    def __init__(self, data, step_function):
        self.data = data
        self.step_function = step_function
        self.available_data = None


    def perform_simulation(self):
        for simulated_date in self.data.index:
            self.available_data = self.get_available_data(self.data, simulated_date)
            self.step_function(self.available_data, simulated_date)

    @staticmethod
    def get_available_data(data, simulated_date):
        data_available_until = simulated_date - Timedelta('1 days')
        available_data = data[:data_available_until]
        return available_data

