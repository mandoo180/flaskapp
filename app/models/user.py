from app import db
from datetime import datetime
from sqlalchemy import select, func


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = { 'extend_existing': True }

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    str_date = db.Column(db.String(8), nullable=False)
    userno = db.Column(db.String(16), nullable=False)
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

    def save(self):
        if self.id:
            self.updated_at = datetime.utcnow()
        else:
            self.str_date = datetime.utcnow().strftime('%Y%m%d')
            self.userno = User.next_userno()
        db.session.add(self)
        db.session.commit()





