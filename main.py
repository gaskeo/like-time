from flask import Flask

import redis

import secrets
import os
from loguru import logger

from blueprints import index, do_search
from api.inst_api import InstApi

logger.add("logs.log", format="{time} {level} {message}", level="INFO", rotation="10 KB", compression="zip")

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

redis_api = redis.Redis(
    password=os.getenv("redis_pass"),
    host=os.getenv("redis_host") or "localhost",
    port=os.getenv("redis_port") or 6379
)

redis_api.ping()  # check connection

app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = secrets.token_hex(24)

app.register_blueprint(index.create_handler())
app.register_blueprint(do_search.create_handler(api, redis_api))

if __name__ == "__main__":
    app.run()
