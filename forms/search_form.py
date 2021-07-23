from wtforms import StringField

from flask_wtf import FlaskForm


class SearchForm(FlaskForm):
    username_or_link = StringField()