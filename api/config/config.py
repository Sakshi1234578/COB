import configparser
import os
from cob.settings import BASE_DIR


class Configuration:
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, 'api/config/config.ini'))
    env = config.get(config.sections()[0], 'Environment')

    def get_Property(key: str) -> str:
        return Configuration.config.get(Configuration.env, key)
