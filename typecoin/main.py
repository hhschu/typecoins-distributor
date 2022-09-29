from random import choices

from typecoin import bonusly, openai, tenor


def send_personalized_thank_you(recipients, total_amount):
    amount = total_amount // len(recipients)
    for handle in recipients:
        name = handle[1:].replace(".", " ")
        message = openai.generate_message(
            f"Write something to thank {name} for the work they have done in the past month!",
            temperature=0.9,
        )
        bonusly.create_bonus(
            amount, [handle], message, img_url=tenor.pick_gif("high five")
        )


def main() -> None:
    myself = "@david.chu"
    core_analytics = [
        "@ilmari.aalto",
        "@iris.miliaraki",
        "@oriol.monereo",
        "@sarthak.jain",
        "@matthew.crooks",
    ]
    team = bonusly.list_users("data enablement") + bonusly.list_users("data science & ai") + core_analytics
    team = list(set(team) - set([myself]))

    balance = bonusly.my_current_balance()
    if balance >= len(team):
        send_personalized_thank_you(team, balance)
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
