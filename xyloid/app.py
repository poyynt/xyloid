from flask import Flask, redirect, url_for
#  from flask_minify import minify
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
import os
from secrets import token_bytes
from .api.api import api
from .auth.auth import auth
from .admin.admin import admin
from .post.post import post
from .db import db, migrate
from .config import config

BASE_PATH = os.environ.get("XYLOID_BASE_PATH", default="/xyloid")
RUN_HOST = os.environ.get("XYLOID_HOST", default="localhost")
RUN_PORT = os.environ.get("XYLOID_PORT", default="24410")

app = Flask(__name__, static_url_path=f"{BASE_PATH}/static")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("XYLOID_DATABASE_URI", default="sqlite:///main.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

if not os.path.exists("xyloid/secret_key"):
    with open("xyloid/secret_key", "wb") as fd:
        fd.write(token_bytes(32))
app.config["SECRET_KEY"] = open("xyloid/secret_key", "rb").read()

app.wsgi_app = ProxyFix(app.wsgi_app)

#  if config["minify"]:
#  minify(app=app, html=False, js=False, cssless=True, static=True)

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(api, url_prefix=f"{BASE_PATH}/api")
app.register_blueprint(auth, url_prefix=f"{BASE_PATH}/auth")
app.register_blueprint(admin, url_prefix=f"{BASE_PATH}/admin")
app.register_blueprint(post, url_prefix=f"{BASE_PATH}/post")


@app.route(f"{BASE_PATH}/")
def index():
    return redirect(url_for('post.index'))


# utility function
def fix_werkzeug_logging():
    from werkzeug.serving import WSGIRequestHandler

    def address_string(self):
        forwarded_for = self.headers.get(
            'X-Forwarded-For', '').split(',')

        if forwarded_for and forwarded_for[0]:
            return forwarded_for[0]
        return self.client_address[0]

    WSGIRequestHandler.address_string = address_string


fix_werkzeug_logging()

with app.test_request_context() as ctx:
    db.create_all()

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if os.environ.get("XYLOID_LOG_FILE", default=None) is not None:
    logging.basicConfig(filename=os.environ.get("XYLOID_LOG_FILE"), level=logging.INFO)

if __name__ == "__main__":
    app.run(host=RUN_HOST, port=RUN_PORT)
