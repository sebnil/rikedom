from zipline.utils.factory import load_from_yahoo as uncached_load_from_yahoo
from zipline.utils.factory import load_bars_from_yahoo as uncached_load_bars_from_yahoo

import caching
from pandas import read_csv
from urllib import urlopen

@caching.region.cache_on_arguments()
def load_from_yahoo(*args, **kwargs):
    return uncached_load_from_yahoo(*args, **kwargs)

@caching.region.cache_on_arguments()
def load_bars_from_yahoo(*args, **kwargs):
    return uncached_load_bars_from_yahoo(*args, **kwargs)


def load_from_SEB(securites, start, stop):
    # http://seb.se/pow/apps/LaddaHemKurser/laddaned_txt.asp?index=&from=140101&tom=150101&fund0=AMF-OBLI&fund1=ROBUR-IDXSVE&format=csv
    #http://seb.se/pow/apps/LaddaHemKurser/laddaned_txt.asp?index=&from=140101&tom=150101&fund1=ROBUR-IDXSVE&format=csv
    url = 'http://seb.se/pow/apps/LaddaHemKurser/laddaned_txt.asp?index=&from=140101&tom=150101&fund1=ROBUR-IDXSVE&format=csv'
    page = urlopen(url).read()
    df = read_csv(page)
    print df
    #print df['Line']