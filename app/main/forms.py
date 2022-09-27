from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField


class PageDownForm(FlaskForm):
    pagedown = PageDownField('Enter your markdown')
    submit = SubmitField('Submit')
