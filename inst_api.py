from requests import session

from json import dumps
from json.decoder import JSONDecodeError


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
        self.query_hash_for_likes = "d5d763b1e2acf209d62d22d184488e57"
        self.query_hash_for_posts = "ea4baf885b60cbf664b34ee760397549"
        self.query_hash_for_post = "2efa04f61586458cef44441f474eee7c"
        self.query_hash_for_account_id = "dbdfd83895d23a4a0b0f68a85486e91c"

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
        try:
            json = g.json()
            if not json["data"]["shortcode_media"]:
                raise KeyError
        except JSONDecodeError:
            return None
        except KeyError:
            return None
        count_liked = json["data"]["shortcode_media"]["edge_liked_by"]["count"]
        count_parsed = 50
        user_liked = [x["node"]["username"] for x in g.json()["data"]["shortcode_media"]["edge_liked_by"]["edges"]]

        while count_liked > count_parsed:
            try:
                json = g.json()
                if not json["data"]["shortcode_media"]:
                    raise KeyError
            except JSONDecodeError:
                continue
            except KeyError:
                return None
            after = json["data"]["shortcode_media"]["edge_liked_by"]["page_info"]["end_cursor"]

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

    def get_user_id_by_post_shortcode(self, shortcode):
        response = self.session.get("https://www.instagram.com/graphql/query/", params={
            "query_hash": self.query_hash_for_post,
            "variables": dumps({"shortcode": shortcode,
                                "child_comment_count": "0",
                                "fetch_comment_count": "0",
                                "parent_comment_count": "0",
                                "has_threaded_comments": True
                                })
        })
        try:
            json = response.json()
        except JSONDecodeError:
            return None
        if json["data"]["shortcode_media"]:
            return json["data"]["shortcode_media"]["owner"]["id"]
        return None

    def get_10_posts_by_user_id(self, user_id):
        variables = {
            "id": user_id,
            "first": 10
        }
        response = self.session.get("https://www.instagram.com/graphql/query", params={
            "query_hash": self.query_hash_for_posts,
            "variables": dumps(variables)
        })
        try:
            posts = response.json()
        except JSONDecodeError:
            return None
        return [x["node"]["shortcode"] for x in posts["data"]["user"]["edge_owner_to_timeline_media"]["edges"]]

    def check_account_exist(self, username):
        return self.session.get(f"https://instagram.com/{username}").status_code == 200
