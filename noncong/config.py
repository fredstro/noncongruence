r"""

"""
import os
import logging
from pymongo.uri_parser import parse_uri

class Config(object):
    def __init__(self):
        self.APP_NAME = 'Subgroups'
        self.TESTING = False
        self.PRODUCTION = False
        self.ENVIRONMENT = 'Default'
        self.SITE_NAME = 'Subgroups and modular forms'
        self.LOG_LEVEL = int(os.getenv('LOG_LEVEL',logging.DEBUG))
        self.DEBUG = True
        #        self.MONGODB_SETTINGS = self.mongo_from_uri(
        #            os.environ.get('MONGO_URI','mongodb://localhost:27017/subgroups'.format(self.ENVIRONMENT.lower())))
        self.MONGODB_SETTINGS = self.mongo_from_uri('mongodb://localhost:27017/subgroups'.format(self.ENVIRONMENT.lower()))

    @staticmethod
    def mongo_from_uri(uri):
        config = parse_uri(uri)
        conn_settings = {
            'db': config['database'],
            'username': config['username'],
            'password': config['password'],
            'host': config['nodelist'][0][0],
            'port': config['nodelist'][0][1]
            }
        return conn_settings


app_config = Config()
