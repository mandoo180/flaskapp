from app import db, login_manager
# from app.exceptions import ValidationError
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import relationship, selectinload, joinedload
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from app.models.key import Key

import hashlib
# import bleach



class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = { 'extend_existing': True }

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    userno = db.Column(db.String(16), nullable=False)
    role = db.Column(db.String(8), nullable=False, default='USER')
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'ADMIN'

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def save(self):
        if self.id:
            self.updated_at = datetime.utcnow()
        else:
            self.userno = Key.getnext('user')
        db.session.add(self)
        db.session.commit()

class AnonymousUser(AnonymousUserMixin):
    
    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
