from wtforms import StringField

from flask_wtf import FlaskForm


class SearchForm(FlaskForm):
    link_or_username = StringField()