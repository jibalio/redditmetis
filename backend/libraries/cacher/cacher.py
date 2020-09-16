from diskcache import Cache
from libraries.constants import SETTINGS

cache=Cache('cache/')

# Cache utilities
def _check(usr):
    usr = usr.lower()
    if usr.lower() in cache:
        return True
    else:
        return False

def try_add_key(usr, b):
    usr = usr.lower()
    if (not _check(usr)):
        cache.set(usr, b, expire=int(SETTINGS["cacher"]["ttl"]), read=False, tag='data')

def get_user_result(usr):
    usr = usr.lower()
    if (_check(usr)):
        return cache[usr]
    else:
        return None


class Cacher:

    def __init__(self, cache_loc):
        self.cache=Cache(cache_loc)

    # Cache utilities
    def check(self, key):
        key = key.lower()
        if key.lower() in self.cache:
            return True
        else:
            return False

    def try_set(self, key, val):
        key = key.lower()
        if (not self.check(key)):
            self.cache.set(
                key, 
                val, 
                expire=int(SETTINGS["cacher"]["ttl"]), 
                read=False, 
                tag='data'
            )
    def get(self, key):
        key = key.lower()
        if (self.check(key)):
            return self.cache[key]
        else:
            return None


