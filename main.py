import os
import random

import requests

BONUSLY_API_TOKEN = os.environ["BONUSLY_API_TOKEN"]
OPEN_AI_API_TOKEN = os.environ["OPEN_AI_API_TOKEN"]
TENOR_API_TOKEN = os.environ["TENOR_API_TOKEN"]


def pick_gif(sess: requests.Session, search_term: str, limit: int = 50) -> str:
    params = {
        "q": search_term,
        "key": TENOR_API_TOKEN,
        "client_key": "typecoin",
        "limit": limit,
    }
    resp = sess.get("https://tenor.googleapis.com/v2/search", params=params)
    content = resp.json()
    gif = random.choice(content["results"])["media_formats"]["gif"]["url"]
    return gif


def generate_message(
    sess: requests.Session,
    prompt: str,
    *,
    temperature: float = 1,
    max_tokens: int = 256,
) -> str:
    payload = {
        "model": "text-davinci-002",
        "prompt": prompt + "\n\n",
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    resp = sess.post("https://api.openai.com/v1/completions", json=payload)
    content = resp.json()

    if err := content.get("error"):
        raise RuntimeError(err["message"])

    return content["choices"][0]["text"].strip()


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
        resp = sess.get("https://bonus.ly/api/v1/users", params=params)
        content = resp.json()
        users = [f'@{user["username"]}' for user in content["result"]]
        recipients.extend(users)
        if len(users) < limit:
            break
        params["skip"] += limit
    return recipients


def current_balace(sess: requests.Session) -> int:
    resp = sess.get("https://bonus.ly/api/v1/users/me")
    content = resp.json()
    return content["result"]["giving_balance"]


def recipients_to_message(recipients: list[str]) -> str:
    if len(recipients) > 2:
        message = f"{', '.join(recipients[:-1])}, and {recipients[-1]}"
    else:
        message = " and ".join(recipients)
    return message


def give(
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

    resp = sess.post("https://bonus.ly/api/v1/bonuses", json={"reason": reason})
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
    with requests.Session() as tenor_sess, requests.Session() as bonusly_sess, requests.Session() as open_ai_sess:
        bonusly_sess.headers.update({"Authorization": f"Bearer {BONUSLY_API_TOKEN}"})
        open_ai_sess.headers.update({"Authorization": f"Bearer {OPEN_AI_API_TOKEN}"})

        team = list_recipients(bonusly_sess, "data enablement") + core_analytics
        team.remove("@david.chu")

        my_balance = current_balace(bonusly_sess)
        if my_balance < len(team):
            raise RuntimeError(
                f"Current balance {my_balance:,} is too low for {len(team)} recipients."
            )

        message = generate_message(
            open_ai_sess,
            "Write something to thank my team for the work they have done in the past month!",
            temperature=0.9,
        )

        give(
            bonusly_sess,
            my_balance,
            team,
            message,
            img_url=pick_gif(tenor_sess, "high five"),
        )


if __name__ == "__main__":
    main()
