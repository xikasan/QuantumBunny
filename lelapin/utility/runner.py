# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, Aer, transpile
from typing import ClassVar, List, Optional, Union

from ..entity.gate import Gate
from ..entity.care import Care
from ..entity.food import Food
from ..entity.lapin import Lapin
from .circuit import prepare, aj
from ..utility import prob

import warnings
warnings.filterwarnings('ignore')


class Backend:

    statevector: str = "statevector_simulator"
    qasm: str = "qasm_simulator"


class Runner:

    BACKEND: ClassVar[Backend] = Backend
    NUM_QUBIT: int = 3

    def __init__(self, lapin: Lapin):
        self.lapin: Lapin = lapin
        self.cares: List[Care] = []
        self.food: Optional[Food] = None

    def care(self, care: Care):
        self.cares.append(care)

    def feed(self, food: Food):
        self.food = food

    def resset_food_care(self):
        self.cares = []
        self.food = None

    def execute(self, backend=Backend.qasm, keep_food_care=False):
        if backend == self.BACKEND.qasm:
            bits = self._exec_qasm()
        if backend == self.BACKEND.statevector:
            res = self._state_prob()
            bits = np.random.choice(np.arange(len(res)), p=res)
            bits = format(bits, "03b")
        bits = self._convert_from_str_to_ints(bits)
        score = self.lapin.sman.observe(bits)
        is_mutated = self._mutate(score)
        res = (score, bits, is_mutated)
        if not keep_food_care:
            self.reset_food_care()
        return res

    def probability(self):
        probs = self._state_prob()
        probs = prob.state_to_prob_for_bit(probs)
        return probs

    def score(self):
        score = self.lapin.sman.score
        return score

    def _state_prob(self):
        res = self._exec_statevector()
        res = self._convert_to_prob(res)
        return res

    def draw(self, output: str = "mpl", ax: Optional[plt.Axes] = None):
        qc, qr = prepare(self.NUM_QUBIT)
        qc, qr = self._build_circuit(qc, qr)
        return qc.draw(output, ax=ax)

    def _exec_qasm(self):
        # prepare circuit and bits
        qc, qr = prepare(self.NUM_QUBIT)
        cr = ClassicalRegister(self.NUM_QUBIT)
        qc.add_register(cr)

        # build and execute
        qc, qr, cr = self._build_circuit(qc, qr, cr)
        sim = Aer.get_backend(self.BACKEND.qasm)

        # post obs process
        res = sim.run(qc, shots=1).result()
        res = res.get_counts()
        res = list(res.keys())[0]
        return res

    def _exec_statevector(self):
        qc, qr = prepare(self.NUM_QUBIT)
        qc, qr = self._build_circuit(qc, qr)
        sim = Aer.get_backend(self.BACKEND.statevector)
        qc = transpile(qc, sim)
        res = sim.run(qc).result()
        vec = res.data()["statevector"]
        vec = np.array(vec)
        return vec

    def _build_circuit(self, qc, qr, cr=None):
        is_statevec = cr is None
        if self.food is not None:
            self.food(qc, qr, wrap=is_statevec)
        self.lapin(qc, qr, wrap=is_statevec)
        [
            care(qc, qr, wrap=is_statevec)
            for care in self.cares
        ]
        if cr is None:
            return qc, qr
        [qc.measure(q, c) for q, c in zip(qr, cr)]
        return qc, qr, cr

    @staticmethod
    def _convert_from_str_to_ints(val):
        return np.array([int(v) for v in val])

    @staticmethod
    def _convert_to_prob(val):
        res = val * aj(val)
        return res.real

    def _mutate(self, bits):
        p = self.lapin.sman.p(bits)
        is_mutated = self.lapin.genome.mutation(p, self.cares[-1])
        return is_mutated


if __name__ == "main":
    print("YES")
