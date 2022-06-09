import os
import random

import requests


def pick_gif(sess: requests.Session, search_term: str, limit: int = 50) -> str:
    params = {
        "q": search_term,
        "key": os.environ["TENOR_API_TOKEN"],
        "client_key": "typecoin",
        "limit": limit,
    }
    resp = sess.get("https://tenor.googleapis.com/v2/search", params=params)
    content = resp.json()
    gif = random.choice(content["results"])["media_formats"]["gif"]["url"]
    return gif
