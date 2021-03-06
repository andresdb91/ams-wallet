# import os

import flask
from flask_cors import CORS

from utils import config
from rabbit import rabbit_service
from wallet import documents
from wallet import routes as wallet_routes


class MainApp:

    instance = None

    def __init__(self):
        # self.flask_app = flask.Flask(__name__, static_folder='../public')
        self.flask_app = flask.Flask(__name__)
        CORS(self.flask_app, support_credentials=True, automatic_options=True)

        # self._init_api_doc()
        # self._init_routes()
        self._init_mongo()
        self._init_rabbit()
        self._init_wallet()

        MainApp.instance = self.flask_app

    # def _init_api_doc(self):
    #     os.system("apidoc -i ../ -o ../public")
    #
    # def _init_routes(self):
    #     # Servidor de archivos estáticos de apidoc
    #     @self.flask_app.route('/<path:path>')
    #     def api_index(path):
    #         return flask.send_from_directory('../public', path)
    #
    #     @self.flask_app.route('/')
    #     def index():
    #         return flask.send_from_directory('../public', "index.html")

    def _init_mongo(self):
        documents.init()

    def _init_rabbit(self):
        rabbit_service.init()

    def _init_wallet(self):
        wallet_routes.init(self.flask_app)

    def get_flask_app(self):
        return self.flask_app

    def start(self, debug=True):
        self.flask_app.run(port=config.get_server_port(), debug=debug)

    @staticmethod
    def wsgi(*args):
        if not MainApp.instance:
            MainApp()

        return MainApp.instance(*args)
