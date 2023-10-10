# imports
from pathlib import Path
from dotenv import load_dotenv, dotenv_values, set_key
from os.path import isfile
from functools import partial

# config
load_dotenv()
env_file_fp = Path(__file__).resolve().parents[1] / '.env'
set_env_key = partial(set_key, env_file_fp, quote_mode='never')

def _init_config():
    """initilize config file if it doesn't exist"""
    if not isfile(env_file_fp):
        env_file_fp.touch(mode=0o600, exist_ok=False)

        set_env_key("SECRET_KEY", "")
        set_env_key("SERVER_NAME", "routelookup.io:5000")
        set_env_key("CURRENT_AIRLINE", "")
        set_env_key("AIRLINE_LIST", "")
        set_env_key("FLIGHTRADAR_USERNAME", "ghub4127@gmail.com")
        set_env_key("FLIGHTRADAR_PASSWORD", "A4zH8B#?R6#LbNnP")
        set_env_key("NAVIGRAPH_USERNAME", "")
        set_env_key("NAVIGRAPH_PASSWORD", "")
        set_env_key("NAVIGRAPH_ENABLED", "Disabled")
        set_env_key("FLIGHTRADAR_API", "")


# initializes config so KeyError is not raised
_init_config()

class Config(object):
    values = dotenv_values(env_file_fp)
    
    DEBUG = True
    DEVELOPMENT = True
    REFRESH = False

    __name__ = 'config'

    __env__ = [
        "SECRET_KEY",
        "SERVER_NAME",
        "CURRENT_AIRLINE",
        "AIRLINE_LIST",
        "AIRLINE_FLIGHTS_LEN",
        "FLIGHTRADAR_USERNAME",
        "FLIGHTRADAR_PASSWORD",
        "NAVIGRAPH_USERNAME",
        "NAVIGRAPH_PASSWORD",
        "NAVIGRAPH_ENABLED",
        "FLIGHTRADAR_API"
    ]

    def __init__(self):
        self.SECRET_KEY = self.values['SECRET_KEY']
        self.SERVER_NAME = self.values['SERVER_NAME']
        self.CURRENT_AIRLINE = self.values['CURRENT_AIRLINE']
        self.AIRLINE_LIST = self.values['AIRLINE_LIST']
        self.AIRLINE_FLIGHTS_LEN = self.values['AIRLINE_FLIGHTS_LEN']
        self.FLIGHTRADAR_USERNAME = self.values['FLIGHTRADAR_USERNAME']
        self.FLIGHTRADAR_PASSWORD = self.values['FLIGHTRADAR_PASSWORD']
        self.NAVIGRAPH_USERNAME = self.values['NAVIGRAPH_USERNAME']
        self.NAVIGRAPH_PASSWORD = self.values['NAVIGRAPH_PASSWORD']
        self.NAVIGRAPH_ENABLED = self.values['NAVIGRAPH_ENABLED']
        self.FLIGHTRADAR_API = self.values['FLIGHTRADAR_API']

    def __setattr__(self, new_kw, val):
        if new_kw in self.__env__:
            set_env_key(new_kw, val)
        super().__setattr__(new_kw, val)

    def cleanup_after_shutdown(self):
        self.CURRENT_AIRLINE = ""
        self.AIRLINE_LIST = ""
        self.AIRLINE_FLIGHTS_LEN = ""
        self.FLIGHTRADAR_API = ""


class DevelopmentConfig(Config):
    """Config to pass thru flask app when developing the app"""
    pass

class ProductionConfig(Config):
    """Config to pass thru flask app when app is in production"""
    DEBUG = False
    DEVELOPMENT = False