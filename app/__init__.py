from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pagedown import PageDown


db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')


    db.init_app(app)
    pagedown = PageDown(app)

    with app.app_context():

        from app.models.post import Post

        db.create_all()
        
        from app.main import main
        app.register_blueprint(main)

        return app

