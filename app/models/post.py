from app import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'post'
    __table_args__ = { 'extend_existing' : True }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title}, body={self.body})"

