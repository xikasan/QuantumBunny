# -*- coding: utf-8 -*-

import numpy as np
import sqlite3
from typing import List, Optional, Tuple


class Lapin:

    def __init__(
            self,
            id_: int,
            name: str,
            genome: List[str],
            points: List[float],
            user_id: int,
            date: str
    ):
        self.id = id_
        self.name = name
        self.genome = genome
        self.points = points
        self.user = user_id
        self.date = date

    def __str__(self):
        ret = f"Lapin[id={self.id} name={self.name} user={self.user}]"
        return ret


def make_table_lapin(dbname: str):
    query_fields = [
        "id integer primary key",
        "name string",
        "genome string",
        "points string",
        "user int",
        "date timestamp default (datetime(current_timestamp,'localtime'))"
    ]
    query = f"create table if not exists lapin({', '.join(query_fields)})"
    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()


class LapinDataManager:

    def __init__(self, dbname: str):
        self.dbname = dbname
        make_table_lapin(dbname)

    def load_lapin(
            self,
            id_: Optional[int] = None,
            name: Optional[str] = None,
            user_id: Optional[int] = None,
    ) -> List[Lapin]:
        conditions = []
        if id_ is not None:
            conditions.append(f"id = '{id_}'")
        if name is not None:
            conditions.append(f"name = '{name}'")
        if user_id is not None:
            conditions.append(f"user = '{user_id}'")

        query = "select * from lapin"
        if len(conditions) > 0:
            str_conditions = " and ".join(conditions)
            query = query + " where " + str_conditions

        with sqlite3.connect(self.dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            lapins = [Lapin(*self.decode_data(row)) for row in cur]

        return lapins

    @staticmethod
    def decode_data(row: tuple) -> Tuple:
        is_from_input = len(row) == 4
        if is_from_input:
            name, str_genome, str_points, user_id = row
        else:
            id_, name, str_genome, str_points, user_id, date = row
        genome = str_genome.split(":")
        points = str_points.split(":")
        points = [float(p) / 100 for p in points]
        if is_from_input:
            return name, genome, points, user_id
        return id_, name, genome, points, user_id, date

    def store_lapin(
            self,
            name: str,
            genome: List[str],
            points: List[float],
            user_id: int,
    ) -> List[Lapin]:
        points = np.asarray(points) * 100
        str_points = ":".join([str(p) for p in points.astype(int)])
        str_genome = ":".join(genome)

        query_base = "insert into lapin (name, genome, points, user) values "
        query_data = "('" + "', '".join([name, str_genome, str_points, str(user_id)]) + "')"
        query = query_base + query_data

        with sqlite3.connect(self.dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()

    def create(
            self,
            name: str,
            genome: List[str],
            points: List[float],
            user_id: int,
    ):
        self.store_lapin(name, genome, points, user_id)
        lapin = self.load_lapin(name=name, user_id=user_id)[0]
        return lapin
