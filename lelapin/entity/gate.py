# -*- coding: utf-8 -*-

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from typing import Callable

from ..utility.circuit import prepare


ROT_DEG = 30.
THETA = np.deg2rad(ROT_DEG)


def q12(qr): return qr[0], qr[1]
def q23(qr): return qr[1], qr[2]
def q31(qr): return qr[2], qr[0]


def mcz(qc, qr):
    qc.h(qr[2])
    qc.mcx(qr[:2], qr[2])
    qc.h(qr[2])


GATES = dict(
    x1=lambda qc, qr: qc.x(qr[0]),
    x2=lambda qc, qr: qc.x(qr[1]),
    x3=lambda qc, qr: qc.x(qr[2]),
    y1=lambda qc, qr: qc.y(qr[0]),
    y2=lambda qc, qr: qc.y(qr[1]),
    y3=lambda qc, qr: qc.y(qr[2]),
    z1=lambda qc, qr: qc.z(qr[0]),
    z2=lambda qc, qr: qc.z(qr[1]),
    z3=lambda qc, qr: qc.z(qr[2]),
    rx1=lambda qc, qr: qc.rx(THETA, qr[0]),
    rx2=lambda qc, qr: qc.rx(THETA, qr[1]),
    rx3=lambda qc, qr: qc.rx(THETA, qr[2]),
    cx12=lambda qc, qr: qc.cx(*q12(qr)),
    cx23=lambda qc, qr: qc.cx(*q23(qr)),
    cx31=lambda qc, qr: qc.cx(*q31(qr)),
    cy12=lambda qc, qr: qc.cy(*q12(qr)),
    cy23=lambda qc, qr: qc.cy(*q23(qr)),
    cy31=lambda qc, qr: qc.cy(*q31(qr)),
    cz12=lambda qc, qr: qc.cz(*q12(qr)),
    cz23=lambda qc, qr: qc.cz(*q23(qr)),
    cz31=lambda qc, qr: qc.cz(*q31(qr)),
    swap=lambda qc, qr: qc.swap(*q31(qr)),
    rxx12=lambda qc, qr: qc.rxx(THETA, *q12(qr)),
    rxx23=lambda qc, qr: qc.rxx(THETA, *q23(qr)),
    rxx31=lambda qc, qr: qc.rxx(THETA, *q31(qr)),
    # ryy12=lambda qc, qr: qc.ryy(THETA, *q12(qr)),
    # ryy23=lambda qc, qr: qc.ryy(THETA, *q23(qr)),
    # ryy31=lambda qc, qr: qc.ryy(THETA, *q31(qr)),
    rzz12=lambda qc, qr: qc.rzz(THETA, *q12(qr)),
    rzz23=lambda qc, qr: qc.rzz(THETA, *q23(qr)),
    rzz31=lambda qc, qr: qc.rzz(THETA, *q31(qr)),
    rzx12=lambda qc, qr: qc.rzx(THETA, *q12(qr)),
    rzx23=lambda qc, qr: qc.rzx(THETA, *q23(qr)),
    rzx31=lambda qc, qr: qc.rzx(THETA, *q31(qr)),
    mcz=lambda qc, qr: mcz(qc, qr),
    # mcx1=lambda qc, qr: qc.mcx(q23, qr[0]),
    # mcx2=lambda qc, qr: qc.mcx(q31, qr[1]),
    # mcx3=lambda qc, qr: qc.mcx(q12, qr[2]),
)


class Gate:

    def __init__(self, label: str = "Gate"):
        self.label = label
        self.gate = self.fetch_gate(label)
        self.parameter = None
        self.trainable = False

    def __call__(
            self,
            qc: QuantumCircuit,
            qr: QuantumRegister,
            *args,
            wrap=False,
            **kwargs
    ):
        if wrap:
            nq = len(qr)
            gate = self.wrap(nq, *args, **kwargs)
            qc.append(gate, qr)
            return gate
        self.process(qc, qr, *args, **kwargs)

    def init(self, nq: int):
        pass

    def process(
            self,
            qc: QuantumCircuit,
            qr: QuantumRegister,
            *args,
            **kwargs
    ):
        self.gate(qc, qr)

    def wrap(self, nq: int, *args, **kwargs):
            qc, qr = prepare(nq)
            self.process(qc, qr, *args, **kwargs)
            wrapped_gate = qc.to_gate()
            wrapped_gate.name = self.label
            return wrapped_gate

    @staticmethod
    def fetch_gate(label: str) -> Callable:
        if label not in GATES.keys():
            raise ValueError(f"{label} is not defined as GATE.")
        label = label.lower()
        return GATES[label]
