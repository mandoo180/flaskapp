import os
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User, Post, Product, Color, ProductColor,\
        Size, ProductSize


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.environ.get('FLASK_ENV') or 'default')

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
    )

# if __name__ == '__main__':
#     app.run()

