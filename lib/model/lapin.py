# -*- coding: utf-8 -*-

import numpy as np
import sqlite3
from typing import List, Optional


class Lapin:

    def __init__(
        self,
        id_: int,
        name: str,
        genome: List[str],
        points: List[float],
        user: int,
        date: str
    ):
        self.id = id_
        self.name = name
        self.genome = genome
        self.points = points
        self.user = user
        self.date = date

    def __str__(self):
        ret = f"Lapin[id={self.id} name={self.name} user={self.user}]"
        return ret



def create_table(dbname: str):
    query = '''
    create table if not exists lapin(
    id integer primary key,
    name string,
    genome string,
    points string,
    user int,
    date timestamp default (datetime(current_timestamp,'localtime'))
    )
    '''

    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()


class LapinDataManager:

    def __init__(self, dbname: str):
        self.dbname = dbname

    @staticmethod
    def create_table(dbname: str):
        db = LapinDataManager(dbname)
        create_table(dbname)
        return db

    def load(
            self,
            id_: Optional[int] = None,
            name: Optional[str] = None,
            user: Optional[int] = None,
    ) -> List[Lapin]:
        conditions = []
        if id_ is not None:
            conditions.append(f"id = {id_}")
        if name is not None:
            conditions.append(f"name = '{name}'")
        if user is not None:
            conditions.append(f"user = {user}")

        query = "select * from lapin"
        if len(conditions) > 0:
            str_conditions = " and ".join(conditions)
            query = query + " where " + str_conditions

        with sqlite3.connect(self.dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            lapins = [Lapin(*row) for row in cur]

        return lapins

    def store(self, name: str, genome: List[str], points: List[float], user_id: int) -> Lapin:
        points = np.asarray(points) * 100
        str_genome = ";".join(genome)
        str_points = ";".join([str(p) for p in points.astype(int)])

        query = f"insert into lapin (name, genome, points, user) values "\
                + f"('{name}', '{str_genome}', '{str_points}', '{user_id}')"

        with sqlite3.connect(self.dbname) as conn:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()

        lapins = self.load(name=name, user=user_id)
        return lapins[0]

    def create(
            self,
            name: str,
            genome: List[str],
            points: List[float],
            user_id: int,
    ) -> Lapin:
        lapin = self.store(name, genome, points, user_id)
        return lapin

