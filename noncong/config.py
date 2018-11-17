r"""

"""
from pymongo.uri_parser import parse_uri
import os
from flask_dotenv import DotEnv
class Config(object):

    @classmethod
    def init_app(self,app):
        """
        Init the app with configuration from .env
        either in the app root folder or at `DOTENV_FILE`
        :param app:
        :return:
        """
        env_file = os.getenv('DOTENV_FILE',os.path.join(app.root_path,'.env'))
        env = DotEnv(app)
        try:
            env.init_app(app,env_file)
        except UserWarning:
            pass
        for key in ['APP_NAME','TESTING','PRODUCTION','ENVIRONMENT','SITE_NAME','LOG_LEVEL','DEBUG','MONGODB_URI']:
            if not app.config.has_key(key):
                raise ValueError,'Configuration key: {0} is missing!'.format(key)
        # app.config['MONGODB_SETTINGS'] = self.mongo_from_uri(app.config.get('MONGODB_URI'))
        mongo_uri = app.config.get('MONGODB_URI', 'mongodb://localhost:27017/subgroups')
        mongo_scattd_uri = app.config.get('MONGODB_SCATTD_URI', mongo_uri)
        app.config['MONGODB_SETTINGS'] = [
            self.mongo_from_uri(mongo_uri, alias="default"),
            self.mongo_from_uri(mongo_scattd_uri, alias="scattering-determinant")
        ]
        if app.config['ENVIRONMENT'].lower()=='testing':
            # Ensure that we don't accidentally overwrite real database while testing.
            app.config['MONGODB_SETTINGS'] = app.config['MONGODB_SETTINGS'].replace("mongodb","mongomock")
            #if 'test' not in app.config['MONGODB_SETTINGS']['db']:
            #    app.config['MONGODB_SETTINGS']['db'] += '_test'

    @staticmethod
    def mongo_from_uri(uri, alias='default'):
        config = parse_uri(uri)
        conn_settings = {
            'db'                   : config['database'],
            'username'             : config['username'],
            'password'             : config['password'],
            'host'                 : config['nodelist'][0][0],
            'port'                 : config['nodelist'][0][1],
            'authentication_source': config.get('options', {}).get('authsource', None),
            'alias'                : alias
        }
        return conn_settings



app_config = Config()
