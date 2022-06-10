import json as json_lib
from functools import partial
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def encode_params(params: dict) -> str:
    param_pairs = []
    for key, value in params.items():
        k = key.encode("utf-8") if isinstance(key, str) else key
        v = value.encode("utf-8") if isinstance(value, str) else value
        param_pairs.append((k, v))
    return urlencode(param_pairs)


def request(
    url: str,
    method: str,
    params: dict = None,
    json: dict = None,
    bearer_token: str = None,
) -> dict:
    headers = {}
    data = None

    if params:
        url = f"{url}?{encode_params(params)}"

    if json:
        headers["Content-Type"] = "application/json"
        data = json_lib.dumps(json).encode("utf-8")

    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"

    try:
        with urlopen(Request(url=url, method=method, headers=headers, data=data)) as f:
            response = f.read().decode("utf-8")
    except HTTPError as err:
        print(err.read())
    else:
        content = json_lib.loads(response)
        return content


get = partial(request, method="GET")
post = partial(request, method="POST")
