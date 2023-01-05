# -*- coding: utf-8 -*-

from qiskit import QuantumCircuit, QuantumRegister
from typing import Callable

from .gate import Gate


FOODS = dict(
    timothy="000",
    carrot="100",
    papaya="010",
    apple="001",
    alfalfa="111"
)


class Food(Gate):

    GATE = FOODS

    def __init__(self, label: str):
        super().__init__(label)

    @staticmethod
    def fetch_gate(label: str) -> Callable:
        if label not in Food.GATE.keys():
            raise ValueError(f"Le lapin n'aime pas {label}.")
        state = FOODS[label]
        gates = [Gate(f"x{i+1}") for i, s in enumerate(state) if s == "1"]
        if len(gates) == 0:
            IGate = Gate("x1")
            IGate.gate = lambda qc, qr: qc.id(qr)
        return lambda qc, qr: [g(qc, qr) for g in gates]
