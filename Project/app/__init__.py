from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import DevelopmentConfig

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
bootstrap = Bootstrap()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.auth import auth_bp
    from app.main import main_bp
    from app.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.errors.handlers import errors
    app.register_blueprint(errors)

    return app