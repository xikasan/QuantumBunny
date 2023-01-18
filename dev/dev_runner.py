# -*- coding: utf-8 -*-

from lelapin.entity.lapin import Lapin
from lelapin.entity.care import Care
from lelapin.entity.food import Food
from lelapin.utility.runner import Runner


def main():
    lapin = Lapin()
    cares = [Care("rub_head")]
    food = Food("carrot")
    runner = Runner(lapin)

    def show_circuit_score_prob():
        print(runner.draw("text"))
        probs = runner.probability()
        scores = runner.score()
        for i in range(lapin.NUM_QUBIT):
            print(f"Q[{i}]:", "{: 4.2f}".format(scores[i]), "{:3.0f} %".format(probs[i] * 100.))

    show_circuit_score_prob()

    for care in cares:
        runner.care(care)
        show_circuit_score_prob()

    runner.feed(food)
    show_circuit_score_prob()


if __name__ == '__main__':
    main()
