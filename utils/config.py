import configparser

config = configparser.ConfigParser()
config.read("wallet.conf")


def get_property(name, default):
    if "DEFAULT" in config:
        if name in config['DEFAULT']:
            return config['DEFAULT'][name]
    return default


def get_server_port():
    return int(get_property('ServerPort', 3101))
