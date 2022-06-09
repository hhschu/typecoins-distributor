import os
import random
from urllib.parse import urljoin

from typecoin import network

URL = "https://tenor.googleapis.com/v2/"
TOKEN = os.environ["TENOR_API_TOKEN"]


def pick_gif(search_term: str, limit: int = 50) -> str:
    params = {"q": search_term, "key": TOKEN, "client_key": "typecoin", "limit": limit}
    content = network.get(urljoin(URL, "search"), params=params)
    gif = random.choice(content["results"])["media_formats"]["gif"]["url"]
    return gif
