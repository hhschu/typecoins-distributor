import requests


def list_users(sess: requests.Session, department: str) -> list[str]:
    users = []
    limit = 100
    params = {
        "skip": 0,
        "user_mode": "normal",
        "department": department.lower(),
        "limit": limit,
    }
    while True:
        resp = sess.get("https://bonus.ly/api/v1/users", params=params)
        content = resp.json()
        users = [f'@{user["username"]}' for user in content["result"]]
        users.extend(users)
        if len(users) < limit:
            break
        params["skip"] += limit
    return users


def my_current_balance(sess: requests.Session) -> int:
    resp = sess.get("https://bonus.ly/api/v1/users/me")
    content = resp.json()
    return content["result"]["giving_balance"]


def recipients_to_message(recipients: list[str]) -> str:
    if len(recipients) > 2:
        message = f"{', '.join(recipients[:-1])}, and {recipients[-1]}"
    else:
        message = " and ".join(recipients)
    return message


def create_bonus(
    sess: requests.Session,
    total_amount: int,
    recipients: list[str],
    message: str,
    img_url: str = None,
) -> None:
    amount = total_amount // len(recipients)
    reason = f"+{amount} {recipients_to_message(recipients)} {message} #wintogether"
    if img_url:
        reason += f" ![]({img_url})"

    print(reason)
    # resp = sess.post("https://bonus.ly/api/v1/bonuses", json={"reason": reason})
    # content = resp.json()

    # if not content["success"]:
    #     raise RuntimeError(content["message"])
