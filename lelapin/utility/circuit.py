# -*- coding: utf-8 -*-

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from typing import Tuple


def prepare(nq: int) -> Tuple[QuantumCircuit, QuantumRegister]:
    qc = QuantumCircuit()
    qr = QuantumRegister(nq)
    qc.add_register(qr)
    return qc, qr
