# -*- coding: utf-8 -*-

from __future__ import annotations

from enum import Enum, auto
from typing import Dict, List, Optional

from ..game.base import Gamer
from ..utility.runner import Runner
from ..entity.lapin import Lapin
from ..entity.care import Care, CARES
from ..entity.food import Food, FOODS


class GameState(Enum):

    INIT = auto()


class GamerBreed(Gamer):

    CARES: Dict[str, str] = CARES
    FOODS: Dict[str, str] = FOODS

    MAX_CARE: int = 5

    def __init__(
            self,
            name: str,
            genome: Optional[List[str]] = None,
    ):
        super().__init__()

