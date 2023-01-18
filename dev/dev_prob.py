# -*- coding: utf-8 -*-
import numpy as np

from lelapin.utility.prob import state_to_prob_for_bit


def main():
    nq = 3
    state_probs = np.random.rand(2 ** nq)
    state_probs = state_probs / np.sum(state_probs)

    state_to_prob_for_bit(state_probs)


if __name__ == '__main__':
    main()
