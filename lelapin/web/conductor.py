# -*- coding: utf-8 -*-

from flask import session, request

from lelapin.entity.lapin import Lapin
from lelapin.manager.genome import GenomeManager
from lelapin.utility.runner import Runner


def rebuild(new_care: str = None, new_food: str = None):
    print("+ "*20)
    print("session:", session.keys())
    print(session.values())
    genome = session["genome"]
    cares = session["cares"]
    food = session["food"]

    if new_care is not None:
        cares.append(cares)
        session["cares"] = cares
    if new_food is not None:
        food = new_food
        session["food"] = food

    lapin = Lapin(genome=genome)
    runner = Runner(lapin)
    runner.reset_food_care()

    if len(cares) > 0:
        [runner.care(care) for care in cares]

    if food is not None:
        runner.food(food)

    return runner
