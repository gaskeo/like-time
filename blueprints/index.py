from flask import Blueprint, render_template


def create_handler():
    app = Blueprint("index", __name__)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")
    return app
