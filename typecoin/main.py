import os

import requests

from typecoin import bonusly, openai, tenor

BONUSLY_API_TOKEN = os.environ["BONUSLY_API_TOKEN"]
OPEN_AI_API_TOKEN = os.environ["OPEN_AI_API_TOKEN"]


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

        team = bonusly.list_users(bonusly_sess, "data enablement") + core_analytics
        team.remove("@david.chu")

        balance = bonusly.my_current_balance(bonusly_sess)
        if balance < len(team):
            raise RuntimeError(
                f"Current balance {balance:,} is too low for {len(team)} recipients."
            )

        message = openai.generate_message(
            open_ai_sess,
            "Write something to thank my team for the work they have done in the past month!",
            temperature=0.9,
        )

        bonusly.create_bonus(
            bonusly_sess,
            balance,
            team,
            message,
            img_url=tenor.pick_gif(tenor_sess, "high five"),
        )


if __name__ == "__main__":
    main()
