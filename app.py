# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request
from datetime import timedelta

from lelapin.game.base import Gamer
from lelapin.entity.lapin import Lapin
from lelapin.manager.genome import GenomeManager
from lelapin.utility.runner import Runner


app = Flask(__name__)

app.secret_key = "MmeUmekodelapin"
app.permanent_session_lifetime = timedelta(minutes=1)

available_cares = ["rub_head", "rub_body", "rub_tail"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game/single", methods=["GET", "POST"])
def game_single():
    selected_care = None
    if request.method == "POST":
        selected_care = request.form.get("care")

    # you have no lapin
    if "genome" not in session:
        print("Generate new lapin")
        gman = GenomeManager("Lapin")
        session["genome"] = [g.label for g in gman.genome]
        session["cares"] = []
        session["food"] = None

    # build lapin from genome
    genome = session["genome"]
    cares = session["cares"]
    food = session["food"]
    if selected_care in available_cares:
        cares.append(selected_care)
        session["cares"] = cares
    print("[load]")
    print("cares:", cares)
    print("food:", food, food is None, type(food))
    lapin = Lapin(genome=genome)
    runner = Runner(lapin)
    runner.reset_food_care()

    # make available care list
    cares_and_flags = [
        [card, 0]
        for card in available_cares
    ]

    # step-0: before care | ready to care
    if len(cares) == 0:
        return render_template(
            "game-single.html",
            cares=[], food=None,
            cards=cares_and_flags
        )

    # step-1: care is selected
    [runner.care(care) for care in cares]
    print("cares:", cares)

    if "food" not in session:
        return render_template(
            "game-single.html",
            cares=cares, food=None,
            cards=cares_and_flags
        )

    food = session["food"]
    runner.feed(food)

    return render_template(
        "game-single.html",
        cares=cares, food=food,
        cards=cares_and_flags
    )


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    app.run(debug=args.debug)
