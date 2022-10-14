from app import db
from datetime import datetime
from sqlalchemy import String, Integer, Column, select, func


class Key(db.Model):
    __tablename__ = 'key'

    id = Column(Integer, primary_key=True)
    prefix = Column(String(8), nullable=False)
    strdate = Column(String(8), nullable=False)
    number = Column(Integer, nullable=False)

    def getkey(self):
        maxnstr = ('000000' + str(self.number))[-6:]
        return f"{prefix}{strdate}{maxnstr}"

    @staticmethod
    def getnext(prefix):
        prefix = prefix.upper()
        today = datetime.utcnow().strftime('%Y%m%d')
        stmt = select(func.max(Key.number)).where(Key.strdate == today)
        maxn = db.session.execute(stmt).scalar() or 0
        maxn += 1
        maxnstr = ('000000' + str(maxn))[-6:]
        return f"{prefix}{today}{maxnstr}"
