from app import db, login_manager
# from app.exceptions import ValidationError
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import relationship, selectinload, joinedload
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin

import hashlib
# import bleach


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = { 'extend_existing': True }

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    str_date = db.Column(db.String(8), nullable=False)
    userno = db.Column(db.String(16), nullable=False)
    role = db.Column(db.String(8), nullable=False)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def next_userno():
        today = datetime.utcnow().strftime('%Y%m%d')
        stmt = select(func.max(User.id)).where(User.str_date == today)
        max_id = db.session.execute(stmt).scalar() or 0
        max_id += 1
        max_id_str = ('000000' + str(max_id))[-6:]
        return f"{today}{max_id_str}"

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def save(self):
        if self.id:
            self.updated_at = datetime.utcnow()
        else:
            self.str_date = datetime.utcnow().strftime('%Y%m%d')
            self.userno = User.next_userno()
        db.session.add(self)
        db.session.commit()

class AnonymousUser(AnonymousUserMixin):
    
    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
