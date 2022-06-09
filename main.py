import os

import requests


def list_recipients(sess: requests.Session, department: str) -> list[str]:
    recipients = []
    limit = 100
    params = {
        "skip": 0,
        "user_mode": "normal",
        "department": department.lower(),
        "limit": limit,
    }
    while True:
        resp = sess.get("https://bonus.ly/api/v1/users", params=params).json()
        users = [f'@{user["username"]}' for user in resp["result"]]
        recipients.extend(users)
        if len(users) < limit:
            break
        params["skip"] += limit
    return recipients


def current_balace(sess: requests.Session) -> int:
    resp = sess.get("https://bonus.ly/api/v1/users/me").json()
    return resp["result"]["giving_balance"]


def recipients_to_message(recipients: list[str]) -> str:
    if len(recipients) > 2:
        message = f"{', '.join(recipients[:-1])}, and {recipients[-1]}"
    else:
        message = " and ".join(recipients)
    return message


def give(sess: requests.Session, total_amount: int, recipients: list[str]) -> None:
    amount = total_amount // len(recipients)
    payload = {"reason": f"+{amount} {recipients_to_message(recipients)} #wintogether"}
    resp = sess.post("https://bonus.ly/api/v1/bonuses", json=payload)
    content = resp.json()

    if not content["success"]:
        raise RuntimeError(content["message"])


def main() -> None:
    core_analytics = [
        "@connell.blackett",
        "@eyuel.muse",
        "@ilmari.aalto",
        "@iris.miliaraki",
        "@oriol.monereo",
        "@sarthak.jain",
        "@matthew.crooks",
    ]
    api_token = os.environ["BONUSLY_API_TOKEN"]
    with requests.Session() as sess:
        sess.headers.update({"Authorization": f"Bearer {api_token}"})
        team = list_recipients(sess, "data enablement") + core_analytics
        team.remove("@david.chu")
        my_balance = current_balace(sess)
        give(sess, my_balance, team)


if __name__ == "__main__":
    main()
