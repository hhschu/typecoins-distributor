from random import choices

from typecoin import bonusly, openai, tenor


def main() -> None:
    myself = "@david.chu"
    core_analytics = [
        "@connell.blackett",
        "@eyuel.muse",
        "@ilmari.aalto",
        "@iris.miliaraki",
        "@oriol.monereo",
        "@sarthak.jain",
        "@matthew.crooks",
    ]
    team = bonusly.list_users("data enablement") + core_analytics
    team = list(set(team) - set([myself]))

    balance = bonusly.my_current_balance()
    if balance > len(team):
        message = openai.generate_message(
            "Write something to thank my team for the work they have done in the past month!",
            temperature=0.9,
        )

        bonusly.create_bonus(
            balance, team, message, img_url=tenor.pick_gif("high five")
        )
    else:
        print(f"Current balance {balance:,} is too low for {len(team)} recipients.")

    left_over = bonusly.my_current_balance()
    bonusly.create_bonus(
        left_over,
        choices(team),
        "You're the lucky winner of my left over coins for this month. Congratulations! 🎉",
        img_url=tenor.pick_gif("wheel of fortune"),
    )


if __name__ == "__main__":
    main()
