import os
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User
from app.models.post import Post
from app.models.product import Product, ProductColor, ProductSize, Color, Size

import sys
import click

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.environ.get('FLASK_ENV') or 'default')

@app.cli.command()
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

@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Post=Post,
        Product=Product,
        Color=Color,
        ProductColor=ProductColor,
        Size=Size,
        ProductSize=ProductSize,
        refresh=refresh,
    )

