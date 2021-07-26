from flask_wtf import FlaskForm

from wtforms import StringField


class SearchForm(FlaskForm):
    username_or_link = StringField()
