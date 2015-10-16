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
import pandas as pd

class TradingSimulator:
    def __init__(self, data, step_function):
        self.data = data
        #self.step_function = step_function
        self.available_data = None
        self.stock_assets = {}
        self.simulated_date = None
        self.interesting_stocks = ['NCC-A.ST']




    def perform_simulation(self):
        for self.simulated_date in self.data.index:
            self.available_data = self.get_available_data(self.data, self.simulated_date)
            self.step(self.available_data, self.simulated_date)
            self.calculate_current_worth()
        self.tear_down()

    def step(self, available_data, simulated_date):
        logging.debug('step base method')

    def calculate_current_worth(self):
        self.worth = self.cash
        for stock_name in self.stock_assets:
            self.worth += self.stock_assets[stock_name] * self.get_price_of_security(stock_name)
        self.recorder.ix[self.simulated_date, 'worth'] = self.worth

    def tear_down(self):
        logging.debug('tear_down base method')

    @staticmethod
    def get_available_data(data, simulated_date):
        data_available_until = simulated_date - Timedelta('1 days')
        available_data = data[:data_available_until]
        return available_data

    def put_order(self, security, number):
        try:
            price = self.get_price_of_security(security)
            cost = price * number
            self.stock_assets[security] = number
            self.cash -= cost
        except KeyError:
            logging.error('Could not perform order since price info does not exist.')

    def sell_order(self, security, number):
        try:
            price = self.get_price_of_security(security)
            sell_price = price * number
            self.stock_assets[security] -= number
            self.cash += sell_price
        except KeyError:
            logging.error('Could not perform order since price info does not exist.')


    def get_price_of_security(self, security):
        price = self.data.ix[self.simulated_date][security]
        return price