# -*- coding: utf-8 -*-


from typing import Optional, Tuple

from ..entity.lapin import Lapin
from ..entity.care import Care
from ..entity.food import Food
from ..utility.runner import Runner


class Gamer:

    def __init__(self, game_id: Optional[int] = None):
        self.id = 0 if game_id is None else game_id
        self.runner: Optional[Runner] = None
        self.result: Tuple = None

    def care(self, care: str):
        care = Care(care)
        self.runner.care(care)

    def feed(self, food: str):
        food = Food(food)
        self.runner.feed(food)

    def execute(self):
        self.result = self.runner.execute(keep_food_care=True)

    @property
    def food(self, as_instance=False):
        food = self.runner.food
        if as_instance:
            return food
        return food.label

    @property
    def cares(self, as_instance=False):
        cares = self.runner.cares
        if as_instance:
            return cares
        return [care.label for care in cares]
