# -*- coding: utf-8 -*-

import numpy as np

from lelapin.entity.lapin import Lapin
from lelapin.manager.genome import GenomeManager
from lelapin.utility.circuit import prepare


def main():
    gm = GenomeManager("Lapin")
    for g in gm:
        print(g)

    qc, qr = prepare(3)
    [gene(qc, qr) for gene in gm]
    print(qc)

    print("---------")

    gm.mutation(0.5, "x1")

    qc, qr = prepare(3)
    [gene(qc, qr) for gene in gm]
    print(qc)


def merge():
    lapin = Lapin()

    qc, qr = prepare(3)
    lapin(qc, qr)
    print(qc)


if __name__ == '__main__':
    merge()
