from flask import Flask, g, request
from flask.ext.babel import Babel
from flask.ext.assets import Environment
from flask.ext.login import LoginManager, current_user
from webassets.loaders import PythonLoader
from skylines.lib import helpers
from .model import User, DBSession
import transaction


def create_app():
    app = Flask(__name__, static_folder='public')
    app.config.from_object('skylines.config.default')

    babel = Babel(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    bundles = PythonLoader('skylines.assets.bundles').load_bundles()
    assets = Environment(app)

    load_path = app.config.get('ASSETS_LOAD_DIR', None)
    if load_path is not None:
        load_url = app.config.get('ASSETS_LOAD_URL', None)
        assets.append_path(load_path, load_url)

    assets.register(bundles)

    return app

app = create_app()

import skylines.views


@app.login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.before_request
def inject_request_identity():
    """ for compatibility with tg2 """

    if not hasattr(request, 'identity'):
        request.identity = {}

    if not current_user.is_anonymous():
        request.identity['user'] = current_user

        request.identity['groups'] = \
            [g.group_name for g in current_user.groups]

        request.identity['permissions'] = \
            [p.permission_name for p in current_user.permissions]


@app.teardown_request
def shutdown_session(exception=None):
    if exception:
        transaction.abort()
    else:
        transaction.commit()

    DBSession.remove()


@app.context_processor
def inject_helpers_lib():
    return dict(h=helpers)


@app.context_processor
def inject_template_context():
    g.identity = request.identity
    return dict(c=g, tmpl_context=g)
