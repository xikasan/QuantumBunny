# -*- coding: utf-8 -*-

import sqlite3
import yaml
from argparse import ArgumentParser

from lib.model.lapin import LapinDataManager

from data.example.lapin import data as lapin_data


db_setting_file = "db.yaml"


def run(args):
    with open(db_setting_file) as fp:
        cf = yaml.safe_load(fp)

    root_path = cf["root"] + "/"

    # make Lapin DB
    lapin_dbname = root_path + cf["lapin"]["name"] + ".db"
    dman_lapin = LapinDataManager.create_table(lapin_dbname)
    # prepare example
    if args.prepare_lapin:
        for ldata in lapin_data:
            dman_lapin.create(*ldata)

    lapins = dman_lapin.load()
    print(lapins)


def prepare_args():
    parser = ArgumentParser()
    parser.add_argument("--prepare-lapin", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = prepare_args()
    run(args)
