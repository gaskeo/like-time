from flask import Blueprint, render_template, jsonify
from forms import SearchForm


from inst_api import InstApi


def create_handler(api: InstApi):
    app = Blueprint("do_search", __name__)
    api = api

    @app.route("/do_search", methods=["POST"])
    def do_search():
        form = SearchForm()
        username_or_link = form.link_or_username.data
        if username_or_link.endswith("/"):
            username_or_link = username_or_link[:-1]
        if "/" in username_or_link:
            username = username_or_link[username_or_link.rfind("/"):]
        else:
            username = username_or_link
        if not api.check_account_exist(username):
            return jsonify({"answer": "пользователь не найден"})

        all_users = dict()
        posts = api.get_10_posts_by_link(f"https://www.instagram.com/{username}/")
        post_links = []
        for i, post in enumerate(posts):
            post_links.append(post)
            users = sorted(api.get_user_liked_post(post))
            for user in users:
                if user in all_users:
                    all_users[user].append(i)
                else:
                    all_users[user] = [i]
        all_users = {user: likes for user, likes in sorted(all_users.items(), key=lambda x: len(x[1]))}
        return jsonify({"answer": "ok", "users": all_users, "posts": post_links})

    return app
