# force python 3.* compability
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
# regular imaports below:
from rikedom.security_loader import load_from_yahoo

import pandas as pd
import numpy as np
from datetime import datetime
from rikedom.simulator import TradingSimulator
import logging
logging.basicConfig(level=logging.DEBUG)
import statsmodels.api as sm

class HodrickPrescottAlgorithm(TradingSimulator):

    def __init__(self):
        super(HodrickPrescottAlgorithm, self).__init__()

        self.cash = 10000 #sek
        self.stock_assets = {}
        self.buy_sell_hold_signal = None

        self.data = None

    def run_algorithm(self, interesting_stocks, start=datetime(2014, 2, 1), end=datetime.now() ):
        logging.info('run_algorithm begin {}'.format(locals()))
        self.interesting_stocks = interesting_stocks

        # get data from yahoo
        self.data = load_from_yahoo(stocks=self.interesting_stocks, indexes={}, start=start, end=end)
        logging.debug('done loading from yahoo. {} {} {}'.format(self.interesting_stocks, start, end))

        self.buy_sell_hold_signal = pd.DataFrame(index=self.data.index, columns=['buy_sell_hold_signal'])
        self.recorder = pd.DataFrame(index=self.data.index, columns=self.interesting_stocks)


        logging.debug('starting to run algo...')
        self.perform_simulation()
        logging.debug('done running algo')


    def step(self, available_data, simulated_date):
        try: self.i += 1
        except: self.i = 1
        logging.debug(self.i),
        if self.i < 3:
            #pass
            return

        if simulated_date == pd.Timestamp('2014-10-15 00:00:00+00:00'):
            pass



        for stock_name in self.interesting_stocks:
            try:
                self.trend, self.xhat = sm.tsa.filters.hpfilter(available_data[[stock_name,]].dropna(), lamb=10000)
            except KeyError:
                logging.error('Could not calculate data on {}, {}. KeyError'.format(stock_name, simulated_date))
                raise

            self.derivitative = np.gradient(self.xhat[stock_name], edge_order=2)
            self.derivitative_2 = np.gradient(self.xhat[stock_name], edge_order=2)
            self.derivitative_2 = np.gradient(self.derivitative_2, edge_order=2)

            signal = 0
            comment = None
            if False and self.derivitative_2[-1] < -0.01: # high momentum sell
                signal = -1
                comment = 'high momentum sell'
            elif self.derivitative[-1] <= 0.2: # safe sell
                signal = -1
                comment = 'threshold sell'
            elif self.derivitative[-1] > 0.2 and self.derivitative_2[-1] > 0: # and derivitative[-2] < 0:
                signal = 1
                comment = 'threshold buy'


            try: assert self.stock_assets[stock_name]
            except: self.stock_assets[stock_name] = 0
            if signal == 1 and self.stock_assets[stock_name] == 0:
                self.put_order(stock_name, 50)
            elif signal == -1 and self.stock_assets[stock_name] > 0:
                self.sell_order(stock_name, 50)

            logging.debug('{}, {}, {}'.format(simulated_date, signal, comment))

            self.buy_sell_hold_signal.ix[simulated_date, stock_name+'.buy_sell_hold_signal'] = signal
            self.recorder.ix[simulated_date, stock_name] = self.stock_assets[stock_name]
            self.recorder.ix[simulated_date, stock_name+'.xhat'] = self.xhat.ix[-1, stock_name]
            self.recorder.ix[simulated_date, stock_name+'.derivitative'] = self.derivitative[-1]
            self.recorder.ix[simulated_date, stock_name+'.derivitative_2'] = self.derivitative_2[-1]

    def tear_down(self):
        self.trend, self.xhat = sm.tsa.filters.hpfilter(self.data[self.interesting_stocks].fillna(0), lamb=10000)
        for stock_name in self.interesting_stocks:
            self.derivitative = np.gradient(self.xhat[stock_name], edge_order=2)
            self.derivitative_2 = np.gradient(self.xhat[stock_name], edge_order=2)
            self.derivitative_2 = np.gradient(self.derivitative_2, edge_order=2)

        pass


# http://python4econ.blogspot.se/2012/05/hodrick-prescott-filter.html