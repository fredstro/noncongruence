r"""

"""
from pymongo.uri_parser import parse_uri
#from os.path import join, dirname
from flask_dotenv import DotEnv
class Config(object):

    @classmethod
    def init_app(self,app):
        """
        Init the app with configuration from .env
        :param app:
        :return:
        """

        env = DotEnv(app)
        env.init_app(app)
        for key in ['APP_NAME','TESTING','PRODUCTION','ENVIRONMENT','SITE_NAME','LOG_LEVEL','DEBUG','MONGODB_URI']:
            if not app.config.has_key(key):
                raise ValueError,'Configuration key: {0} is missing!'.format(key)
        app.config['MONGODB_SETTINGS'] = self.mongo_from_uri(app.config.get('MONGODB_URI'))
        if app.config['ENVIRONMENT'].lower()=='testing':
            # Ensure that we don't accidentally overwrite real database while testing.
            app.config['MONGODB_SETTINGS'] = app.config['MONGODB_SETTINGS'].replace("mongodb","mongomock")
            #if 'test' not in app.config['MONGODB_SETTINGS']['db']:
            #    app.config['MONGODB_SETTINGS']['db'] += '_test'

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
