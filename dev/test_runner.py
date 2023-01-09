# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


from lelapin.entity.lapin import Lapin
from lelapin.entity.care import Care
from lelapin.entity.food import Food
from lelapin.utility.runner import Runner


def main():
    lapin = Lapin()
    cares = [Care("rub_head")]
    food = Food("carrot")
    runner = Runner(lapin)
    [runner.care(care) for care in cares]
    runner.feed(food)

    fig, ax = plt.subplots()
    runner.draw(ax=ax)
    plt.show()

    res = runner.execute()
    print(res)


if __name__ == "__main__":
    main()
