import os
from typing import List

import requests


def current_balace(sess: requests.Session) -> int:
    resp = sess.get("https://bonus.ly/api/v1/users/me").json()
    return resp["result"]["giving_balance"]


def recipients_to_message(recipients: List[str]) -> str:
    if len(recipients) > 2:
        message = f"{', '.join(recipients[:-1])}, and {recipients[-1]}"
    else:
        message = " and ".join(recipients)
    return message


def give(sess: requests.Session, total_amount: int, recipients: List[str]) -> None:
    amount = total_amount // len(recipients)
    payload = {
        "reason": f"+{amount} {recipients_to_message(recipients)} for great #teamwork #yourock!"
    }
    resp = sess.post("https://bonus.ly/api/v1/bonuses", json=payload)
    resp.raise_for_status()


def main() -> None:
    team = ["@manuel.romero", "@pablo.reynel"]
    with requests.Session() as sess:
        sess.headers.update({"Authorization": f"Bearer {os.environ['BONUSLY_API_TOKEN']}"})
        balance = current_balace(sess)
        give(sess, balance, team)


if __name__ == "__main__":
    main()
