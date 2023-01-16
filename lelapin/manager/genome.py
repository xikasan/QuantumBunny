# -*- coding: utf-8 -*-

import numpy as np

from typing import List, Optional, Union
from ..entity.gate import Gate, GATES, ROT_DEG


class GenomeManager:

    GATES = GATES
    NUM_QUBIT: int = 3

    def __init__(
            self,
            name: str,
            genome: Optional[List["str"]] = None,
            size: Optional[int] = 3
    ):
        self.genome = self._decode(name, genome, size)

        self._it_index: int = None

    def __next__(self):
        if self._it_index >= self.size:
            raise StopIteration()

        ret = self.genome[self._it_index]
        self._it_index += 1
        return ret

    def __iter__(self):
        self._it_index = 0
        return self

    @property
    def size(self):
        return len(self.genome)

    def _decode(
            self,
            name: Optional[str] = "Lapin",
            genome: Optional[List[str]] = None,
            size: Optional[int] = 5
    ):
        # decode from genome
        if genome is not None:
            genome = [Gate(gene) for gene in genome]
            return genome

        # generate at random
        genome_init = sum([
            [
                f"rx{i+1}"
                for _ in range(np.random.randint(0, 180 // ROT_DEG, dtype=int))
            ] for i in range(self.NUM_QUBIT)
        ], [])
        genome_body = np.random.choice(list(self.GATES.keys()), size, replace=True).tolist()
        genome = [Gate(g) for g in sum([genome_init, genome_body], [])]
        return genome

    def mutation(self, prob: float, gene: Union[str, Gate]) -> bool:
        assert prob >= 0
        # not mutate
        if prob <= np.random.rand():
            return False

        # mutate
        if not isinstance(gene, Gate):
            gene = Gate(gene)

        self.genome.append(gene)

