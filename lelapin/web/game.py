# -*- coding: utf-8 -*-

from flask import session, request

from lelapin.entity.lapin import Lapin
from lelapin.manager.genome import GenomeManager
from lelapin.utility.runner import Runner


KEY_LAPIN_INFO = "lapin_info"
KEY_GAME_STATE = "game_state"
KEY_CARDS = "cards_and_flags"
KEY_CARDS_CARE = "care"
KEY_CARDS_FOOD = "food"


def create_new_lapin():
    lapin_name = session.get("name", "lapin")
    gman = GenomeManager(lapin_name)
    lapin_image = "image.png"
    lapin_genome = [g.label for g in gman.genome]
    return dict(
        name=lapin_name,
        image=lapin_image,
        genome=lapin_genome,
    )


def load_lapin():
    if KEY_LAPIN_INFO in session.keys():
        lapin_info = session[KEY_LAPIN_INFO]
    else:
        lapin_info = create_new_lapin()
    lapin = Lapin(lapin_info["genome"])
    return lapin, lapin_info


def load_state():
    if KEY_GAME_STATE in session.keys():
        return session[KEY_GAME_STATE]
    return dict(
        food=None,
        cares=[],
        scores=[]
    )


def load_cards_and_flags():
    if KEY_CARDS in session:
        return session[KEY_CARDS]
    return {
        KEY_CARDS_CARE: [],
        KEY_CARDS_FOOD: [],
    }


def save_lapin(lapin_info):
    session[KEY_LAPIN_INFO] = lapin_info


def save_state(game_state):
    session[KEY_GAME_STATE] = game_state
