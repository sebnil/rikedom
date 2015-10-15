# force python 3.* compability
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
# regular imaports below:
import sys
sys.path.append('../../zipline-test/') # add parent directory to path
from rikedom.security_loader import load_from_yahoo
from rikedom import caching

from pandas import Timedelta
import pandas as pd
import numpy as np
from datetime import datetime
from rikedom.simulator import TradingSimulator
import logging
logging.basicConfig(level=logging.DEBUG)
import statsmodels.api as sm

security=None

buy_sell_hold_signal = None

def step(available_data, simulated_date):
    pass


def run_algorithm(stock='AAPL', start=datetime(2014, 2, 1), end=datetime.now() ):
    logging.info('run_algorithm begin {}'.format(locals()))
    global security, buy_sell_hold_signal
    security = stock

    # get data from yahoo
    data = load_from_yahoo(stocks=[security], indexes={}, start=start, end=end)
    logging.debug('done loading from yahoo. {} {} {}'.format(security, start, end))

    buy_sell_hold_signal = pd.DataFrame(index=data.index, columns=['buy_sell_hold_signal'])

    logging.debug('init algo...')
    hp_filter_algo = TradingSimulator(data, step_function=step)


    logging.debug('starting to run algo...')
    hp_filter_algo.perform_simulation()
    logging.debug('done running algo')


def step(available_data, simulated_date):
    try: step.i += 1
    except: step.i = 1
    logging.debug(step.i)
    if step.i < 10:
        return

    #logging.debug('simulated date is: {}'.format(simulated_date))
    global security, buy_sell_hold_signal

    trend, xhat = sm.tsa.filters.hpfilter(available_data[[security,]].dropna(), lamb=10000)
    derivitative = np.gradient(xhat[security], edge_order=2)
    derivitative_2 = np.gradient(xhat[security], edge_order=2)
    derivitative_2 = np.gradient(derivitative_2, edge_order=2)

    signal = None
    comment = None
    if derivitative_2[-1] < -0.0001: # high momentum sell
        signal = False
        comment = 'high momentum sell'
    elif derivitative[-1] < 0.1: # safe sell
        signal = False
        comment = 'threshold sell'
    elif derivitative[-1] > 0.1: # and derivitative[-2] < 0:
        signal = True
        comment = 'threshold buy'
    try:
        buy_sell_hold_signal.ix[simulated_date]['buy_sell_hold_signal'] = signal
        logging.error('OK on {}'.format(simulated_date))
    except:
        logging.error('error on {}'.format(simulated_date))
        pass

    pass

