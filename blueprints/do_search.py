from flask import Blueprint, render_template, jsonify, request
from forms import SearchForm

from urllib.parse import urlparse

from inst_api import InstApi


def create_handler(api: InstApi):
    app = Blueprint("do_search", __name__)
    api = api

    @app.route("/do_search", methods=["POST"])
    def do_search():
        form = SearchForm()
        username_or_link = form.username_or_link.data
        if not username_or_link:
            return jsonify({"answer": "error", "error-message": "empty"})
        username_or_link = username_or_link.replace("@", "")
        if "/" not in username_or_link:
            user_id = api.get_user_id_by_username(username_or_link)
            if not user_id:
                return jsonify({"answer": "error", "error-message": "пользователь не найден,"
                                                                    " возмжоно аккаунт приватный"})
        else:
            parse_link = urlparse(username_or_link)
            path = parse_link.path
            sections = tuple(filter(len, path.split("/")))

            if "p" in sections:
                user_id = api.get_user_id_by_post_shortcode(sections[-1])
                if not user_id:
                    return jsonify({"answer": "error", "error-message": "пост не найден, возмжоно аккаунт приватный"})
            else:
                user_id = api.get_user_id_by_username(sections[-1])
                if not user_id:
                    return jsonify({"answer": "error", "error-message": "пользователь не найден,"
                                                                        " возмжоно аккаунт приватный"})

        all_users = dict()
        posts = api.get_10_posts_by_user_id(user_id)
        if not posts:
            return jsonify({"answer": "error", "error-message": "пост не найден, возмжоно аккаунт приватный"})
        post_links = []
        for i, post in enumerate(posts):
            post_links.append(post)
            users = api.get_user_liked_post(post)
            if not users:
                return jsonify({"answer": "error", "error-message": "пост не найден, возможно аккаунт приватный"})
            for user in users:
                if user in all_users:
                    all_users[user].append(i)
                else:
                    all_users[user] = [i]
        all_users = {user: likes for user, likes in sorted(all_users.items(), key=lambda x: len(x[1]))}
        return jsonify({"answer": "ok", "users": all_users, "posts": post_links, "error-message": ""})

    return app
