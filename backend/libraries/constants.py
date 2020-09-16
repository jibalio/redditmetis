import configparser

def cast_bool(val):
    return val.lower()=="true" or val.lower()=="yes" or val==1

SETTINGS = None
MAINTENANCE = None
PRODUCTION = None
LOADCACHE = None

if SETTINGS==None:
    SETTINGS = configparser.ConfigParser()
    SETTINGS.read('redditmetis.ini')
    if MAINTENANCE == None:
        MAINTENANCE=cast_bool(SETTINGS["general"]["maintenance"].lower())
    if PRODUCTION==None:
        PRODUCTION=cast_bool(SETTINGS["general"]["production"])
    if LOADCACHE==None:
        LOADCACHE=cast_bool(SETTINGS["cacher"]["enable"])


