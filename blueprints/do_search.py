from flask import Blueprint, render_template, jsonify
from forms import SearchForm


from inst_api import InstApi


def create_handler(api: InstApi):
    app = Blueprint("do_search", __name__)
    api = api

    @app.route("/do_search", methods=["POST"])
    def do_search():
        form = SearchForm()
        shortcode_or_link = form.shortcode_or_link.data
        if shortcode_or_link.endswith("/"):
            shortcode_or_link = shortcode_or_link[:-1]
        if "/" in shortcode_or_link:
            shortcode = shortcode_or_link[shortcode_or_link.rfind("/") + 1:]
        else:
            shortcode = shortcode_or_link

        all_users = dict()
        user_id = api.get_user_id_by_post_shortcode(shortcode)
        posts = api.get_10_posts_by_user_id(user_id)
        post_links = []
        for i, post in enumerate(posts):
            post_links.append(post)
            users = api.get_user_liked_post(post)
            for user in users:
                if user in all_users:
                    all_users[user].append(i)
                else:
                    all_users[user] = [i]
        all_users = {user: likes for user, likes in sorted(all_users.items(), key=lambda x: len(x[1]))}
        return jsonify({"answer": "ok", "users": all_users, "posts": post_links})

    return app
