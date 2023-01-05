# -*- coding: utf-8 -*-

from qiskit import QuantumCircuit, QuantumRegister
from typing import Callable

from .base import Gate


CARES = dict(
    rub_head="x1",
    rub_body="x2",
    rub_tail="x3",
    groom_head="cx12",
    groom_body="cx23",
    groom_tail="cx31",
    hug="mcz"
)


class Care(Gate):

    GATE = CARES

    def __init__(self, name: str = "Care"):
        super().__init__(name)

    @staticmethod
    def fetch_gate(label: str) -> Callable:
        if label not in Care.GATE.keys():
            raise ValueError(f"Le lapin n'aime pas {label}")
        care = Gate(CARES[label])
        return care

