"""Initialize app."""
from flask import Flask
from flask_login import LoginManager
from flask_session import Session

from FAST.database import db

login_manager = LoginManager()

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('FAST.config.Config')
    if not app.config["SQLALCHEMY_DATABASE_URI"]:
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////tmp/test.db'

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # from . import routes
        from FAST import auth
        # from .assets import compile_assets

        # # Register Blueprints
        # app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        # Create Database Models
        db.create_all()

        # Compile static assets
        if app.config['FLASK_ENV'] == 'development':
            compile_assets(app)

        return app

app = create_app()
sess = Session()

app.config["SECRET_KEY"] = "FAST_SDD"
app.config["SESSION_TYPE"] = "sqlalchemy"

sess.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

from FAST import routes
