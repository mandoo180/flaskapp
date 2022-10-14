from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()

def create_app(config_name):
    # app = Flask(__name__, instance_relative_config=False)
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    # pagedown = PageDown(app)

    # with app.app_context():

    # from app.models.user import User, Post, Product, Color, ProductColor
    

    # db.create_all()
    
    from app.main import main as main_blueprint
    from app.auth import auth as auth_blueprint
    from app.admin import admin as admin_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app

