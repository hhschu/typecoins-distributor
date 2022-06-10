import os
from urllib.parse import urljoin

from typecoin import network

URL = "https://bonus.ly/api/v1/"
TOKEN = os.environ["BONUSLY_API_TOKEN"]


def list_users(department: str, *, limit: int = 100) -> list[str]:
    users = []
    params = {
        "skip": 0,
        "user_mode": "normal",
        "department": department.lower(),
        "limit": limit,
    }
    while True:
        content = network.get(urljoin(URL, "users"), params=params, bearer_token=TOKEN)
        users = [f'@{user["username"]}' for user in content["result"]]
        users.extend(users)
        if len(users) < limit:
            break
        params["skip"] += limit  # type: ignore
    return users


def my_current_balance() -> int:
    content = network.get(urljoin(URL, "users/me"), bearer_token=TOKEN)
    return content["result"]["giving_balance"]


def recipients_to_message(recipients: list[str]) -> str:
    if len(recipients) > 2:
        message = f"{', '.join(recipients[:-1])}, and {recipients[-1]}"
    else:
        message = " and ".join(recipients)
    return message


def create_bonus(
    total_amount: int, recipients: list[str], message: str, img_url: str = None
) -> None:
    amount = total_amount // len(recipients)
    reason = f"+{amount} {recipients_to_message(recipients)} {message} #wintogether"
    if img_url:
        reason += f" ![]({img_url})"

    content = network.post(urljoin(URL, "bonuses"), json={"reason": reason}, bearer_token=TOKEN)

    if not content["success"]:
        raise RuntimeError(content["message"])
