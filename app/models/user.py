from app import db
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import relationship, selectinload, joinedload


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


class Post(db.Model):
    __tablename__ = 'post'
    __table_args__ = { 'extend_existing' : True }

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post(id={self.id}, user_id={self.user_id}, title={self.title}, body={self.body})"


class ProductColor(db.Model):
    __tablename__ = 'product_color'
    pid = db.Column(db.ForeignKey('product.id'), primary_key=True)
    cid = db.Column(db.ForeignKey('color.id'), primary_key=True)
    color = db.relationship('Color', viewonly=True)

class ProductSize(db.Model):
    __tablename__ = 'product_size'
    pid = db.Column(db.ForeignKey('product.id'), primary_key=True)
    sid = db.Column(db.ForeignKey('size.id'), primary_key=True)
    size = db.relationship('Size', viewonly=True)

class Color(db.Model):
    __tablename__ = 'color'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Size(db.Model):
    __tablename__ = 'size'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    label = db.Column(db.String(8), nullable=False)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    colors = db.relationship('ProductColor', viewonly=True)

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


    @staticmethod
    def refresh():
        db.drop_all()
        db.create_all()
        colors = 'red', 'blue', 'white', 'black', 'orange'
        sizes = ('small', 's'), ('medium', 'm'), ('large', 'l')
        for color in colors:
            c = Color(name=color)
            c.save()
        for size in sizes:
            s = Size(name=size[0], label=size[1])
            s.save()
        cids = [color.id for color in Color.query.all()]
        sids = [size.id for size in Size.query.all()]
        p = Product(name='knowledge is the key')
        p2 = Product(name='mickey mouse')

        Product.save(p, cids=cids, sids=sids)
        Product.save(p2, cids=cids, sids=sids)

    def delete(self):
        ProductColor.query.filter_by(pid=self.id).delete()
        ProductSize.query.filter_by(pid=self.id).delete()
        db.session.delete(self)
        db.session.commit()
