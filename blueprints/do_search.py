from flask import Blueprint, render_template
from forms import SearchForm
from json import dumps

from inst_api import InstApi


def create_handler(api: InstApi):
    app = Blueprint("do_search", __name__)
    api = api

    @app.route("/do_search", methods=["POST"])
    def do_search():
        form = SearchForm()
        print(form.link_or_username.data)
        return dumps({"status": "ok"})

    return app
