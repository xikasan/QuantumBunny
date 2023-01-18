# -*- coding: utf-8 -*-

import numpy as np
from typing import List, Union


class ScoreManager:

    NUM_QUBIT = 3

    def __init__(
            self,
            max: float = 2.,
            min: float = -1.,
            factor: float = 9.,
            bias: float = 6.,
    ):
        assert max > min
        self.max = max
        self.min = min
        self._scores = np.zeros(self.NUM_QUBIT)

        assert factor > 0
        assert bias >= 0
        self.a = factor
        self.d = bias / 10

        self.reset()

    def reset(self):
        delta = self.max - self.min
        scores = np.random.rand(self.NUM_QUBIT) * delta + self.min
        self._scores = scores
        return scores

    def p(self, x):
        return 1 / (1 + np.exp(
            -1 * self.a * (x / self.max / self.NUM_QUBIT - self.d)
        ))

    def observe(self, bits: Union[List, np.ndarray]) -> float:
        bits = np.asarray(bits)
        return self._scores @ bits

    @property
    def score(self) -> np.ndarray:
        return self._scores.copy()
