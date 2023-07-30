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
    START = auto()
    CARED = auto()
    FOOD_SELECTED = auto()
    FEED = auto()
    DONE = auto()

    @classmethod
    def is_possible_care(cls, state: GameState) -> bool:
        ret = state is cls.START or state is cls.CARED
        return ret

    @classmethod
    def is_possible_feed(cls, state: GameState) -> bool:
        ret = state is cls.START or state is cls.CARED
        return ret


class GamerSingle(Gamer):

    CARES: Dict[str, str] = CARES
    FOODS: Dict[str, str] = FOODS

    MAX_CARE: int = 3

    def __init__(
            self,
            name: str,
            genome: Optional[List[str]] = None
    ):
        super().__init__()
        self.runner = Runner(
            Lapin(name=name, genome=genome)
        )
        self.state: GameState = GameState.INIT

    def step_0_reset(self):
        self.state = GameState.START
        self.runner.reset_food_care()

    def step_1_care(self, care: str):
        assert GameState.is_possible_care(self.state)
        assert care in list(self.CARES.keys())
        assert self.MAX_CARE >= self.runner.num_care()
        care = Care(care)
        self.state = GameState.CARED
        self.runner.care(care)

    def step_2_feed(self, food: str):
        assert GameState.is_possible_feed(self.state)
        assert food in list(self.FOODS.keys())
        food = Food(food)
        self.state = GameState.FOOD_SELECTED
        self.runner.feed(food)

    def step_3_execute(self):
        assert self.state is GameState.FOOD_SELECTED
        self.state = GameState.FEED
        self.execute()
        self.state = GameState.DONE
