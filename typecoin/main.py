from typecoin import bonusly, openai, tenor


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
    team = bonusly.list_users("data enablement") + core_analytics
    team.remove("@david.chu")

    balance = bonusly.my_current_balance()
    if balance < len(team):
        raise RuntimeError(
            f"Current balance {balance:,} is too low for {len(team)} recipients."
        )

    message = openai.generate_message(
        "Write something to thank my team for the work they have done in the past month!",
        temperature=0.9,
    )

    bonusly.create_bonus(balance, team, message, img_url=tenor.pick_gif("high five"))


if __name__ == "__main__":
    main()
