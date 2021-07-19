import os

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

all_users = dict()
api = InstApi(cs)
posts = api.get_10_posts_by_link("https://www.instagram.com/instagram/")

for i, post in enumerate(posts):
    users = sorted(api.get_user_liked_post(post))
    for user in users:
        if user in all_users:
            all_users[user].append(i)
        else:
            all_users[user] = [i]
for user in sorted(all_users.keys()):
    print(user.ljust(50, " "), end="|")
    for i in range(10):
        if i in all_users[user]:
            print(" + ", end="|")
        else:
            print("   ", end="|")
    print()