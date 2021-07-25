from flask import Blueprint, jsonify, request

from redis import Redis

from urllib.parse import urlparse

from loguru import logger

from api.inst_api import InstApi
from forms.search_form import SearchForm


def create_handler(api: InstApi, redis_api: Redis):
    app = Blueprint("do_search", __name__)

    @app.route("/do_search", methods=["POST"])
    def do_search():
        if redis_api.get(request.remote_addr):
            return jsonify({"answer": "error", "error-message": "много запросов шлешь, меня в инсте заблокируюст... "
                                                                "5 секунд между запросами должно быть..."})
        form = SearchForm()
        username_or_link = form.username_or_link.data
        if not username_or_link:
            logger.error(f"{request.remote_addr} empty request")
            return jsonify({"answer": "error", "error-message": "empty"})

        redis_api.set(name=request.remote_addr, value=1, ex=5)

        username_or_link = username_or_link.replace("@", "")
        if "/" not in username_or_link:
            user_id = api.get_user_id_by_username(username_or_link)
            if not user_id:
                logger.error(f"{request.remote_addr} invalid username caught: {user_id}")
                return jsonify({"answer": "error", "error-message": "пользователь не найден,"
                                                                    " возмжоно аккаунт приватный"})
        else:
            parse_link = urlparse(username_or_link)
            path = parse_link.path
            sections = tuple(filter(len, path.split("/")))

            if "p" in sections:
                user_id = api.get_user_id_by_post_shortcode(sections[-1])
                if not user_id:
                    logger.error(f"{request.remote_addr} invalid username caught: {user_id}")
                    return jsonify({"answer": "error", "error-message": "пост не найден, возмжоно аккаунт приватный"})
            else:
                user_id = api.get_user_id_by_username(sections[-1])
                if not user_id:
                    logger.error(f"{request.remote_addr} invalid username caught: {user_id}")
                    return jsonify({"answer": "error", "error-message": "пользователь не найден,"
                                                                        " возмжоно аккаунт приватный"})

        all_users = dict()
        posts = api.get_10_posts_by_user_id(user_id)
        if not posts:
            logger.error(f"{request.remote_addr} invalid posts caught: {user_id}")
            return jsonify({"answer": "error", "error-message": "посты не найдены, возмжоно аккаунт приватный"})
        post_links = []
        for i, post in enumerate(posts):
            post_links.append(post)
            users = api.get_user_liked_post(post)
            if not users:
                logger.error(f"{request.remote_addr} invalid posts caught: {user_id}")
                return jsonify({"answer": "error", "error-message": "пост не найден, возможно аккаунт приватный"})
            for user in users:
                if user in all_users:
                    all_users[user].append(i)
                else:
                    all_users[user] = [i]
        all_users = {user: likes for user, likes in sorted(all_users.items(), key=lambda x: len(x[1]))}
        logger.info(f"{request.remote_addr} ok: {user_id}")
        return jsonify({"answer": "ok", "users": all_users, "posts": post_links, "error-message": ""})

    return app
