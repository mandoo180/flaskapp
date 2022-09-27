from flask import render_template
from app.main import main
from app.main.forms import PageDownForm
from markdown import markdown


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PageDownForm()
    if form.validate_on_submit():
        text = form.pagedown.data
        html = markdown(text, extensions=['tables'])
        print(text)
        print(html)
    return render_template('/index.html', form=form)
