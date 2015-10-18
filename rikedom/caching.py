import pickle
import hashlib
import binascii
from dogpile.cache import make_region
from dogpile.cache.api import NoValue
from dogpile.cache.proxy import ProxyBackend
#import dogpile.cache.api
import os
import logging
logging.basicConfig(level=logging.DEBUG)
from pickle import PicklingError

def my_key_generator(namespace, fn):
    if namespace is None:
        namespace = '%s:%s' % (fn.__module__, fn.__name__)
    else:
        namespace = '%s:%s|%s' % (fn.__module__, fn.__name__, namespace)

    def generate_key(*args, **kwargs):
        try:
            picklestring = pickle.dumps((namespace, args, kwargs))
        except (PicklingError, TypeError):
            picklestring = pickle.dumps((str(namespace), str(args), str(kwargs)))
        dk = hashlib.sha256(picklestring)
        key = dk.hexdigest()
        return key

    return generate_key


class MyProxy(ProxyBackend):
    def set(self, key, value):
        try:
            key = key.replace(' ', '_')
        except:
            pass

        logging.debug('Setting Cache Key: %s' % key)
        try:
            self.proxied.set(key, value)
        except:
            logging.warning('Cache setting error. Will ignore setting of cache on this item.')
            #raise

    def get(self, key):
        try:
            key = key.replace(' ', '_')
        except:
            pass

        try:
            logging.debug('Getting Cache Key: %s' % key)
            return self.proxied.get(key)
        except:
            logging.warning('Cache getting error. Will ignore getting of cache on this item.')
            #raise


# default to None to get scope of region variable
region = None
try:
    region = make_region(function_key_generator=my_key_generator).configure(
                'dogpile.cache.pylibmc',

                expiration_time=3600 * 100,
                arguments={
                    'url': ["127.0.0.1:8001"],
                },
                wrap=[MyProxy]
            )
except:
    pass
try:
    # test if cache is working
    region.set('foo', 'bar')
    assert region.get('foo') == 'bar'
except:
    try:
        logging.info('Could not use memcached. Trying redis...')
        region = make_region(function_key_generator=my_key_generator).configure(
            'dogpile.cache.redis',
            expiration_time=3600,
            arguments={
                'host': 'localhost',
                'port': 6379,
                'db': 0,
                'redis_expiration_time': 3600,   # 1 hour
                'distributed_lock': True
            },
            wrap=[MyProxy]
        )
        # test if cache is working now
        region.set('foo', 'bar')
        assert region.get('foo') == 'bar'
        logging.debug('Redis cache is working')
    except:
        try:
            logging.info('Could not use memcached. Trying file cache...')
            region = make_region(function_key_generator=my_key_generator).configure(
                'dogpile.cache.dbm',
                expiration_time=3600,
                arguments={
                    "filename": "{dir}/cachefile.dbm".format(dir=os.path.dirname(os.path.realpath(__file__)))
                },
                wrap=[MyProxy]
            )
            # test if cache is working now
            region.set('foo', 'bar')
            assert region.get('foo') == 'bar'
            logging.debug('File cache is working')
        except:
            logging.info('Could not use dbm. Trying memory_pickle...')
            region = make_region(function_key_generator=my_key_generator).configure(
                'dogpile.cache.memory_pickle',
                expiration_time=3600,
                arguments={
                    "filename": "{dir}/cachefile.dbm".format(dir=os.path.dirname(os.path.realpath(__file__)))
                },
                wrap=[MyProxy]
            )