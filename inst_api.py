from requests import session

from json import dumps


class InstApi:
    headers = {
        'user-agent':
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 '
            '(KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; '
            'en-US; scale=2.00; 828x1792; 165586599)'
    }

    def __init__(self, cookies):
        self.session = session()
        [self.session.cookies.set(n, m) for n, m in cookies.items()]
        self.inst_text = self.session.get("https://instagram.com").text
        self.query_hash_for_likes = "d5d763b1e2acf209d62d22d184488e57"
        self.query_hash_for_posts = "ea4baf885b60cbf664b34ee760397549"

    def get_user_liked_post(self, post_shortcode):
        variables = {
            "shortcode": f"{post_shortcode}",
            "include_reel": False,
            "first": 50
        }
        g = self.session.get("https://www.instagram.com/graphql/query/", params={
            "query_hash": self.query_hash_for_likes,
            "variables": dumps(variables)
        })
        count_liked = g.json()["data"]["shortcode_media"]["edge_liked_by"]["count"]
        count_parsed = 50
        user_liked = [x["node"]["username"] for x in g.json()["data"]["shortcode_media"]["edge_liked_by"]["edges"]]

        while count_liked > count_parsed:
            after = g.json()["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]

            variables = {
                "shortcode": f"{post_shortcode}",
                "include_reel": False,
                "first": 50,
                "after": f"{after}"
            }

            g = self.session.get("https://www.instagram.com/graphql/query/", params={
                "query_hash": self.query_hash_for_likes,
                "variables": dumps(variables)
            })

            user_liked += [x["node"]["username"] for x in g.json()["data"]["shortcode_media"]["edge_liked_by"]["edges"]]
            count_parsed += 50
        return user_liked

    def get_user_id_by_link(self, link):
        account_text = self.session.get(link).text
        print(account_text)
        user_id = account_text[account_text.index("profilePage_") + len("profilePage_"):]
        user_id = user_id[:user_id.index('"')]
        return user_id

    def get_10_posts_by_link(self, link):
        user_id = self.get_user_id_by_link(link)
        variables = {
            "id": user_id,
            "first": 10
        }
        posts = self.session.get("https://www.instagram.com/graphql/query", params={
            "query_hash": self.query_hash_for_posts,
            "variables": dumps(variables)
        }).json()

        return [x["node"]["shortcode"] for x in posts["data"]["user"]["edge_owner_to_timeline_media"]["edges"]]

    def check_account_exist(self, username):
        return self.session.get(f"https://instagram.com/{username}").status_code == 200
