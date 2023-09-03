# -*- coding: utf-8 -*-

import pandas as pd
import argparse
from qbunny.model.lapin import Lapin, LapinDataManager


def run(args):
    ldm = LapinDataManager("data/lapin.db")

    if args.dummy:
        lapin_dummy = pd.read_csv(
            "data/dummy/dummy_lapin.csv",
            names=["name", "genome", "points", "user"]
        )
        for i, lapin in lapin_dummy.iterrows():
            ldm.create(*ldm.decode_data(tuple(
                [lapin["name"], lapin["genome"], lapin["points"], lapin["user"]]
            )))
    [print(l) for l in ldm.load_lapin()]


def prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dummy", action="store_true")

    return parser.parse_args()


if __name__ == '__main__':
    args = prepare_args()
    run(args)
