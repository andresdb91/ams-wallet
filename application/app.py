import os

import flask
from flask_cors import CORS

from rabbit.rabbit_service import RabbitService
from utils import config
from wallet.routes import WallerRoutes


class MainApp:

    def __init__(self):
        self.flask_app = flask.Flask(__name__, static_folder='../public')
        CORS(self.flask_app, support_credentials=True, automatic_options=True)

        self.rabbit = RabbitService()
        self.rabbit.init()

        self._init_routes()
        self._init_api_doc()

    def _init_routes(self):
        # Servidor de archivos estáticos de apidoc
        # Por el momento se genera con ../auth/node_modules/.bin/apidoc -i ./ -o public
        @self.flask_app.route('/<path:path>')
        def api_index(path):
            return flask.send_from_directory('../public', path)

        @self.flask_app.route('/')
        def index():
            return flask.send_from_directory('../public', "index.html")

    def _init_api_doc(self):
        os.system("apidoc -i ./ -o ./public")

    def get_flask_app(self):
        return self.flask_app

    def start(self):
        self.flask_app.run(port=config.get_server_port())
