# -*- coding: utf-8 -*-

import numpy as np


def state_to_prob_for_bit(state_prob: np.ndarray) -> np.ndarray:
    ns = len(state_prob)
    nq = int(np.log2(ns))

    state_as_binary_str = [
        format(i, f"0{nq}b")[::-1]
        for i in range(ns)
    ]
    is_the_qubit_one = np.array([
        [
            b[i] == "1"
            for b in state_as_binary_str
        ] for i in range(nq)
    ])
    qubit_probs = [
        np.sum(state_prob[selector])
        for selector in is_the_qubit_one
    ]
    return qubit_probs
