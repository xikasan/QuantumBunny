# -*- coding: utf-8 -*-

from lelapin.game.breeding import GamerBreeding


# temp parameters to go
name: str = "UsaUsa"
dmode: str = "text"


def print_score_prob(runner):
    scores = runner.score()
    probs = runner.probability()
    for i, (s, p) in enumerate(zip(scores, probs)):
        print(f"Q[{i}]:", "{: 4.2f}".format(s), "{:3.0f} %".format(p * 100.))


def def_show(gamer):
    def f():
        print(gamer.runner.draw(dmode))
        print_score_prob(gamer.runner)
        print("- "* 60)
    return f


gamer = GamerBreeding(name)
show = def_show(gamer)

print("name:", gamer.runner.lapin.name)
show()

gamer.step_0_reset()
show()

gamer.step_1_care("rub_head")
show()

gamer.step_2_feed("apple")
show()

gamer.step_3_execute()
show()

score, bits, is_mutated = gamer.result
print("score : {: 5.2f}".format(score))
print(f"bits  : [{bits[0]}, {bits[1]}, {bits[2]}]")
print("mutate:", is_mutated)
