# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request
from datetime import timedelta

from lelapin.game.base import Gamer
from lelapin.entity.lapin import Lapin
from lelapin.manager.genome import GenomeManager
from lelapin.utility.runner import Runner
from lelapin.game.base import Gamer
from lelapin.web.conductor import rebuild
from lelapin.web.game import *

app = Flask(__name__)

app.secret_key = "MmeUmekodelapin"
app.permanent_session_lifetime = timedelta(minutes=1)


# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +
# for debug
available_cares = ["rub_head", "rub_body", "rub_tail"]
available_foods = ["carrot", "timothy"]
#
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +

# Parameter
# 画像の初期位置
x1 = 10
y1 = 440
x2 = 110
y2 = 440

# おやつ画像をドロップできる位置を指定
dA_snack_x1 = 109
dA_snack_y1 = 297.5
dA_snack_x2 = 198
dA_snack_y2 = 390.5

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    # for "POST":
    selected_care = request.form.get("care", None)
    selected_food = request.form.get("food", None)
    print(selected_care, selected_food)

    # lapin
    lapin, lapin_info = load_lapin()
    runner = Runner(lapin)
    gamer = Gamer()
    gamer.runner = runner

    # game state
    game_state = load_state()
    game_state["scores"] = runner.score().tolist()
    if selected_care is not None:
        game_state["cares"].append(selected_care)
    if selected_food is not None:
        game_state["food"] = selected_food
    print("game_state:", game_state)

    # apply cards
    score = None
    [gamer.care(care) for care in game_state["cares"]]
    if game_state["food"] is not None:
        gamer.feed(game_state["food"])
        gamer.execute()
    print("result:", gamer.result)

    cards_and_flags = load_cards_and_flags()
    # mod for debug
    cards_and_flags[KEY_CARDS_CARE] = [
        dict(label=c, is_selected=1 if c in game_state["cares"] else 0)
        for c in available_cares
    ]
    cards_and_flags[KEY_CARDS_FOOD] = [
        dict(label=f, is_selected=1 if f == game_state["food"] else 0)
        for f in available_foods]

    # write to session
    save_lapin(lapin_info)
    save_state(game_state)

    return render_template(
        "game.html",
        lapin_info=lapin_info,
        game_state=game_state,
        cards_and_flags=cards_and_flags,
        score=score,
        x1=x1, y1=y1, x2=x2, y2=y2, dA_snack_x1=dA_snack_x1, dA_snack_y1=dA_snack_y1, dA_snack_x2=dA_snack_x2, dA_snack_y2=dA_snack_y2
    )


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
    print("food:", food)
    lapin = Lapin(genome=genome)
    runner = Runner(lapin)
    runner.reset_food_care()

    # make available care list
    cares_and_flags = [
        [card, 1 if card in cares else 0]
        for card in available_cares
    ]
    foods_and_flags = [
        [card, 1 if card in cares else 0]
        for card in available_foods
    ]
    print(cares_and_flags)
    print(foods_and_flags)

    cards_and_flags = foods_and_flags + cares_and_flags
    print("=-"*20)
    print("[debug]")
    print(cards_and_flags)
    print("- "*20)

    # step-0: before care | ready to care
    if len(cares) == 0:
        return render_template(
            "game-single.html",
            cares=[], food=None,
            cards=cards_and_flags
        )

    # step-1: care is selected
    [runner.care(care) for care in cares]
    print("cares:", cares)

    if "food" not in session:
        return render_template(
            "game-single.html",
            cares=cares, food=None,
            cards=cards_and_flags
        )

    food = session["food"]
    runner.feed(food)

    return render_template(
        "game-single.html",
        cares=cares, food=food,
        cards=cards_and_flags
    )


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    app.run(debug=args.debug)
