from app import db 
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from datetime import datetime


class ProductColor(db.Model):
    __tablename__ = 'product_color'
    pid = Column(ForeignKey('product.id'), primary_key=True)
    cid = Column(ForeignKey('color.id'), primary_key=True)
    color = relationship('Color', viewonly=True)

class ProductSize(db.Model):
    __tablename__ = 'product_size'
    pid = Column(ForeignKey('product.id'), primary_key=True)
    sid = Column(ForeignKey('size.id'), primary_key=True)
    size = relationship('Size', viewonly=True)

class Color(db.Model):
    __tablename__ = 'color'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Size(db.Model):
    __tablename__ = 'size'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    label = Column(String(8), nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(16), nullable=False)
    colors = relationship('ProductColor', viewonly=True)

    @staticmethod
    def save(product, **kwargs):

        if product.id:
            ProductColor.query.filter_by(pid=product.id).delete()
            ProductSize.query.filter_by(pid=product.id).delete()
        cids = kwargs.get('cids', [])
        sids = kwargs.get('sids', [])

        db.session.add(product)
        db.session.commit()

        for cid in cids:
            pcolor = ProductColor(pid=product.id, cid=cid)
            db.session.add(pcolor)
        for sid in sids:
            psize = ProductSize(pid=product.id, sid=sid)
            db.session.add(psize)
        db.session.commit()

    def delete(self):
        ProductColor.query.filter_by(pid=self.id).delete()
        ProductSize.query.filter_by(pid=self.id).delete()
        db.session.delete(self)
        db.session.commit()
