# -*- coding: utf-8 -*-

import numpy as np

from lelapin.manager.score import ScoreManager


def main():
    sm = ScoreManager()
    print(sm.points)

    bits = np.random.choice([0, 1], 3, replace=True)
    score = sm.observe(bits)

    print("Bots :", bits)
    print("Score:", score)

    p = sm.p(score)
    print("prob :", p)


if __name__ == '__main__':
    main()
