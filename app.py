# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, jsonify
from datetime import timedelta

from lelapin.game.base import Gamer
from lelapin.entity.lapin import Lapin
from lelapin.manager.genome import GenomeManager
from lelapin.utility.runner import Runner
from lelapin.web.conductor import rebuild
from lelapin.web.game import *


app = Flask(__name__)

app.secret_key = "MmeUmekodelapin"
app.permanent_session_lifetime = timedelta(hours=24)


# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +
# for debug
available_cares = ["rub_head", "rub_body", "rub_tail"]
available_foods = ["carrot", "timothy"]
#
# + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + +

# セッションからゲーム状態を取得し、存在しない場合は初期化
def initialize_game_state(session, runner):
    if 'game_state' not in session:
        session['game_state'] = {
            "cares": [],
            "food": None,
            "scores": runner.score().tolist()
        }
    return session['game_state']

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    data = request.get_json()
    try:
        selected_food = data['selected_food']
    except:
        selected_food = None

    try:
        selected_care = data['selected_care']
    except:
        selected_care = None

    # lapin
    lapin, lapin_info = load_lapin()
    runner = Runner(lapin)
    gamer = Gamer()
    gamer.runner = runner

    game_state = initialize_game_state(session, runner)

    # ゲーム状態を更新
    if selected_care:
        game_state["cares"] = selected_care
    if selected_food:
        game_state["food"] = selected_food

    # apply cards
    score = 0.0
    result_bit_list = [0, 0, 0]
    [gamer.care(care) for care in game_state["cares"]]

    if game_state["food"] is not None:
        gamer.feed(game_state["food"])
        gamer.execute()

    if gamer.result:
        result_bit_list = [gamer.result[1][0], gamer.result[1][1], gamer.result[1][2]]
        score = result_bit_list[0] * game_state['scores'][0] + result_bit_list[1] * game_state['scores'][1] + result_bit_list[2] * game_state['scores'][2]

    result_data = {
        "result_score": score,
        "result_bit_list": result_bit_list
    }

    cards_and_flags = load_cards_and_flags()
    cards_and_flags[KEY_CARDS_CARE] = [
        dict(label=c, is_selected=1 if c in game_state.get("cares", []) else 0)
        for c in available_cares
    ]
    cards_and_flags[KEY_CARDS_FOOD] = [
        dict(label=f, is_selected=1 if f == game_state.get("food") else 0)
        for f in available_foods]

    # セッションにゲーム状態を保存
    session['game_state'] = game_state

    save_lapin(lapin_info)
    save_state(game_state)

    return render_template(
        "game.html",
        lapin_info=lapin_info,
        game_state=game_state,
        cards_and_flags=cards_and_flags,
        score=score,
        result_data=result_data, # `gamer.result`をテンプレートに渡す
    )

@app.route("/call_from_ajax", methods = ["POST"])
def calc_and_return_result():
    if request.method == "POST":
        # 計算実行
        try:
            data = request.get_json()
            selected_food = data.get('selected_food', None)
            selected_care = data.get('selected_care', [])

            # lapin
            lapin, lapin_info = load_lapin()
            runner = Runner(lapin)
            gamer = Gamer()
            gamer.runner = runner

            game_state = initialize_game_state(session, runner)
            game_state["cares"] = selected_care if selected_care else []
            game_state["food"] = selected_food

            score = None
            [gamer.care(care) for care in game_state["cares"]]

            if game_state["food"] is not None:
                gamer.feed(game_state["food"])
                gamer.execute()

            if gamer.result:
                result_bit_list = [int(gamer.result[1][0]), int(gamer.result[1][1]), int(gamer.result[1][2])]
                score = result_bit_list[0] * game_state['scores'][0] + result_bit_list[1] * game_state['scores'][1] + result_bit_list[2] * game_state['scores'][2]

            message = {
                "result_score": score,
                "result_bit_list": result_bit_list if gamer.result else None
            }
            # セッションにゲーム状態を保存
            session['game_state'] = game_state

            save_lapin(lapin_info)
            save_state(game_state)

        except Exception as e:
            message = str(e)

    return jsonify({"answer": message})

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
