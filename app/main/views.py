from flask import render_template, request
from flask_login import login_required
from app.main import main
# from app.main.forms import PageDownForm
from markdown import markdown


# @main.route('/', methods=['GET', 'POST'])
# def index():
#     form = PageDownForm()
#     if form.validate_on_submit():
#         text = form.pagedown.data
#         html = markdown(text, extensions=['tables'])
#         print(text)
#         print(html)
#     return render_template('/index.html', form=form)

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('/index.html')

@main.route('/posts', methods=['GET'])
def posts():
    return render_template('main/posts.html')

@main.route('/products', methods=['GET'])
def products():
    return render_template('main/products.html')

@main.route('/orders', methods=['GET'])
def orders():
    return render_template('main/products.html')

@main.route('/success')
def success():
    args = request.args
    payment_key = args['paymentKey']
    order_no = args['orderId']
    amount = args['amount']
    print(payment_key, order_no, amount)
    return render_template('/success.html')

@main.route('/fail')
def fail():
    args = request.args
    code = args['code']
    message = args['message']
    order_no = args['orderId']
    print(code, message, order_no)
    return render_template('/fail.html')

