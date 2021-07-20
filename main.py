from flask import Flask

import secrets
import os

from blueprints import index, do_search
from inst_api import InstApi

cs = {
    "csrftoken": os.getenv("csrftoken"),
    "ds_user_id": os.getenv("ds_user_id"),
    "ig_did": os.getenv("ig_did"),
    "ig_nrcb": "1",
    "mid": os.getenv("mid"),
    'rur': os.getenv("rur"),
    "sessionid": os.getenv("sessionid"),
    'shbid': os.getenv("shbid"),
    'shbts': os.getenv("shbts")
}
api = InstApi(cs)
app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_hex(24)

app.register_blueprint(index.create_handler())
app.register_blueprint(do_search.create_handler(api))

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0", use_reloader=True, debug=True)
