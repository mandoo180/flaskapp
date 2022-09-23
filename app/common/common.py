from sqlalchemy import select, func
from app import db


def get_max_id(model):
    stmt = select(func.max(model.id))
    return db.session.execute(stmt).scalar()
