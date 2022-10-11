from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_pagedown import PageDown
from config import config


db = SQLAlchemy()

def create_app(config_name):
    # app = Flask(__name__, instance_relative_config=False)
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    # pagedown = PageDown(app)

    # with app.app_context():

    # from app.models.user import User, Post, Product, Color, ProductColor
    

    # db.create_all()
    
    from app.main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app

