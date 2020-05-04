# -*- coding: utf-8 -*-
"""
Construct visualization-JSON from dpdb-database results.

See https://www.postgresqltutorial.com/postgresql-python/connect/
and reference
https://github.com/VaeterchenFrost/dp_on_dbs.git

IPython adds it's own handler to the root logger, see
https://stackoverflow.com/questions/24259952/logging-module-does-not-print-in-ipython

Calling python directly prints the logging as per logging.basicConfig!


Copyright (C) 2020  Martin Röbke

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import itertools
import json
import abc
import logging
import pathlib

from time import sleep
from configparser import ConfigParser
from typing import Optional, Iterable, Iterator, TypeVar
import psycopg2 as pg
from more_itertools import locate


from dijkstra import bidirectional_dijkstra as find_path
from dijkstra import convert_to_adj

__author__ = "Martin Röbke <martin.roebke@tu-dresden.de>"
__status__ = "development"
__version__ = "0.2"
__date__ = "20 April 2020"

logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s"
    "[%(filename)s:%(lineno)d] %(message)s",
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.WARNING)

LOGGER = logging.getLogger(__name__)


PSYCOPG2_8_5_TASTATUS = {
    pg.extensions.TRANSACTION_STATUS_IDLE:
        ('TRANSACTION_STATUS_IDLE ',
         '(The session is idle and there is no current transaction.)'),

        pg.extensions.TRANSACTION_STATUS_ACTIVE:
        ('TRANSACTION_STATUS_ACTIVE ',
         '(A command is currently in progress.)'),

        pg.extensions.TRANSACTION_STATUS_INTRANS:
        ('TRANSACTION_STATUS_INTRANS ',
         '(The session is idle in a valid transaction block.)'),

        pg.extensions.TRANSACTION_STATUS_INERROR:
        ('TRANSACTION_STATUS_INERROR ',
         '(The session is idle in a failed transaction block.)'),

        pg.extensions.TRANSACTION_STATUS_UNKNOWN:
        ('TRANSACTION_STATUS_UNKNOWN ',
         '(Reported if the connection with the server is bad.)')
}

_T = TypeVar('_T')


def flatten(iterable: Iterable[Iterable[_T]]) -> Iterator[_T]:
    """ Flatten at first level.

    Turn ex=[[1,2],[3,4]] into
    [1, 2, 3, 4]
    and [ex,ex] into
    [[1, 2], [3, 4], [1, 2], [3, 4]]
    """
    return itertools.chain.from_iterable(iterable)


def good_db_status() -> tuple:
    """Indicating a good db status to proceed."""
    return (pg.extensions.TRANSACTION_STATUS_IDLE,
            pg.extensions.TRANSACTION_STATUS_INTRANS)


def read_cfg(cfg_file, section) -> dict:
    """Read the config file and return the result.

    Works for both .ini and .json files but
    assumes json-format if the ending is NOT .ini
    """
    if pathlib.Path(cfg_file).suffix.lower() == ".ini":
        iniconfig = ConfigParser()
        iniconfig.read(cfg_file)
        result = dict()
        result["host"] = iniconfig.get(section, "host", fallback="localhost")
        result["port"] = iniconfig.getint(section, "port", fallback=5432)
        result["database"] = iniconfig.get(
            section, "database", fallback="logicsem")
        result["user"] = iniconfig.get(section, "user", fallback="postgres")
        result["password"] = iniconfig.get(section, "password")
        result["application_name"] = iniconfig.get(
            section, "application_name", fallback="dpdb-admin")
        return {section: result}

    # default behaviour
    with open(cfg_file) as jsonfile:
        return json.load(jsonfile)


def config(filename='database.json', section='postgresql') -> dict:
    """Return the database config as JSON"""
    cfg = read_cfg(filename, section)
    if section in cfg:
        db_config = cfg[section]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    LOGGER.info("Read db_config['%s'] from '%s'", section, filename)
    return db_config


class IDpdbVisuConstruct(metaclass=abc.ABCMeta):
    """Interface for parsing database results from dynamic programming
    into the JSON used for visualizing the solution steps
    on the tree decomposition.
    See details for i-face impl in https://realpython.com/python-interface/
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'read_labeldict') and
                callable(subclass.read_labeldict) and
                hasattr(subclass, 'read_timeline') and
                callable(subclass.read_timeline) and
                hasattr(subclass, 'read_edgearray') and
                callable(subclass.read_edgearray) or
                NotImplemented)

    @abc.abstractmethod
    def read_edgearray(self) -> list:
        """Return the edges between the bags."""
        raise NotImplementedError

    @abc.abstractmethod
    def read_labeldict(self) -> list:
        """Construct the corresponding labels for each bag."""
        raise NotImplementedError

    @abc.abstractmethod
    def read_timeline(self, edgearray) -> list:
        """Read from td_node_status and the edearray to
            - create the timeline of the solving process
            - construct the path and solution-tables used during solving.
        """
        raise NotImplementedError


class DpdbSharpSatVisu(IDpdbVisuConstruct):
    """Implementation of the JSON-Construction for the SharpSat problem."""

    def __init__(self, db: pg.extensions.connection, problem: int):
        """db : psycopg2.connection
            database to read from.
        problem : int
            index of the problem.
        """
        LOGGER.debug("Creating %s for problem %d.",
                     self.__class__.__name__, problem)
        self.problem = problem
        # wait for good connection
        status = db.get_transaction_status()
        sleeptimer = 0.5
        while status not in good_db_status():
            logging.warning("Waiting %fs for DB connection in status %s",
                            sleeptimer, PSYCOPG2_8_5_TASTATUS[status])
            sleep(sleeptimer)
            status = db.get_transaction_status()

        self.connection = db

    def read_clauses(self) -> list:
        """Return the clauses used for satiyfiability.
        Variables are counted from 1 and negative if negated in the clause.
        For example:

            [{
                "id" : 1,
                "list" : [ 1, -4, 6 ]
            },...]
        """
        with self.connection.cursor() as cur:  # create a cursor
            cur.execute(
                "SELECT * FROM public.p{:d}_sat_clause".format(self.problem))
            result = cur.fetchall()
            result_cleaned = [
                [i + 1 if x[i] else -(i + 1) for i in
                 locate(x, lambda p: p is not None)] for x in result
            ]
            clauses_edges = [{"id": i, "list": item}
                             for (i, item) in enumerate(result_cleaned, 1)]
            return clauses_edges

    def read_labeldict(self) -> list:
        """
        Read from '_td_bag' the edges and 'td_node_status' tables the labels
        for the bags.

        Returns
        -------
        list
            The filled labeldict for visualization.

        """
        with self.connection.cursor() as cur:  # create a cursor
            labeldict = []
            # check bag numbering:
            cur.execute(
                "SELECT bag FROM public.p{:d}_td_bag group by bag".format(
                    self.problem))
            bags = sorted(list(flatten(cur.fetchall())))
            LOGGER.debug("bags: %s", bags)
            for bag in bags:
                cur.execute(
                    "SELECT node FROM public.p{:d}_td_bag WHERE bag=%s".format(
                        self.problem), (bag,))
                nodes = list(flatten(cur.fetchall()))
                cur.execute(
                    "SELECT start_time,end_time-start_time "
                    "FROM public.p{:d}_td_node_status WHERE node=%s".format(
                        self.problem), (bag,))
                start_time, dtime = cur.fetchone()
                labeldict.append(
                    {"id": bag, "items": nodes, "labels":
                     [str(nodes),
                      "dtime=%.4fs" % dtime.total_seconds(),
                      start_time.strftime("%D %T")
                      ]})
            return labeldict

    def read_timeline(self, edgearray) -> list:
        """
        Read from td_node_status and the edearray to
        - create the timeline of the solving process
        - construct the path and solution-tables used during solving.

        Parameters
        ----------
        edgearray : array of pairs of bagids
            Representing the tree-like structure between all bag-ids.
            It is assumed that all ids are included in this array.
            Example: [(2, 1), (3, 2), (4, 2), (5, 4)]

        Returns
        -------
        result : array
            array of bagids and eventually solution-tables.

        """
        with self.connection.cursor() as cur:  # create a cursor
            timeline = list()
            adj = convert_to_adj(edgearray)
            cur.execute(
                "SELECT node FROM public.p{}_td_node_status".format(
                    self.problem))
            order_solved = list(flatten(cur.fetchall()))
            # tour sol -> through result nodes along the edges
            last = order_solved[-1]
            startpath = find_path(adj, last, order_solved[0])
            timeline = [[bag] for bag in startpath[1]]
            # add the other bags in order_solved to the timeline
            last = order_solved[0]
            for bag in order_solved:
                path = find_path(adj, last, bag)
                for intermed in path[1][1:]:
                    timeline.append([intermed])
                # query column names
                #  deepcode ignore Sqli: general query, inserting integers
                cur.execute(
                    "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_NAME = 'p{:d}_td_node_{:d}'".format(
                        self.problem, bag))
                column_names = list(flatten(cur.fetchall()))
                LOGGER.debug("column_names %s", column_names)
                # get solutions
                #  deepcode ignore Sqli: general query, inserting integers
                cur.execute(
                    "SELECT * FROM public.p{:d}_td_node_{:d}".format(self.problem, bag))
                solution_raw = cur.fetchall()
                LOGGER.debug("solution_raw %s", solution_raw)
                # check for nulled variables - assuming whole columns are
                # nulled:
                columns_notnull = [column_names[i] for i, x in
                                   enumerate(solution_raw[0]) if x is not None]
                solution = [bag,
                            [[columns_notnull,
                              *[[int(v) for v in row if v is not None]
                                for row in solution_raw]],
                             "sol bag " + str(bag),
                             "sum: " + str(sum([li[-1]
                                                for li in solution_raw])),
                             True]]
                timeline.append(solution)
                last = bag

            return timeline

    def read_edgearray(self):
        with self.connection.cursor() as cur:  # create a cursor
            cur.execute(
                "SELECT node,parent FROM public.p{}_td_edge".format(
                    self.problem))
            result = cur.fetchall()
            return result


class DpdbMinVcVisu(DpdbSharpSatVisu):
    """TODO
    """
    pass


def connect() -> pg.extensions.connection:
    """Connect to the PostgreSQL database server using the params from config
    """
    conn = None
    try:
        # read connection parameters
        params = config()
        db_name = params["database"]

        LOGGER.info("Connecting to the PostgreSQL database '%s'...", db_name)
        conn = pg.connect(**params)

        with conn.cursor() as cur:  # create a cursor

            # display the PostgreSQL database server version
            LOGGER.info('PostgreSQL database version:')
            cur.execute('SELECT version()')

            db_version = cur.fetchone()
            LOGGER.info(db_version)

    except (Exception, pg.DatabaseError) as error:
        LOGGER.error(error)
        raise error
    return conn


def read_problem(problem: int, connection: pg.extensions.connection) -> tuple:
    """TODO
    """
    with connection.cursor() as cur:  # create a cursor
        cur.execute(
            "SELECT num_vars,num_clauses,model_count FROM "
            "public.problem_sharpsat WHERE id=%s", (problem,))
        num_vars, num_clauses, model_count = cur.fetchone()
        cur.execute("SELECT name,type,num_bags,tree_width,num_vertices,"
                    "setup_start_time,calc_start_time,end_time FROM "
                    "public.problem WHERE id=%s", (problem,))
        (name, ptype, num_bags, tree_width, num_vertices,
         setup_start_time, calc_start_time, end_time) = cur.fetchone()
        return (num_vars, num_clauses, model_count, ptype, num_bags)
    raise pg.DatabaseError("Could not get a cursor for read_problem.")


def create_json(problem: int) -> Optional[dict]:
    """Create the JSON for the specified Problem instance."""

    LOGGER.info("creating JSON for problem %s.", problem)

    try:
        with connect() as connection:
            # get type of problem
            (num_vars, num_clauses, model_count, ptype,
             num_bags) = read_problem(problem, connection)
            # select the valid constructor for the problem
            constructor: IDpdbVisuConstruct

            if ptype == "SharpSat":
                constructor = DpdbSharpSatVisu(connection, problem)

                clauses_edges = constructor.read_clauses()
                incidence_graph = {
                    "varNameOne": "c_",
                    "varNameTwo": "v_",
                    "inferPrimal": True,
                    "edges": clauses_edges}

                # create tree_dec_json
                labeldict = constructor.read_labeldict()
                edgearray = constructor.read_edgearray()
                tree_dec_json = {
                    "bagpre": "bag %s",
                    "edgearray": edgearray,
                    "labeldict": labeldict,
                    "numVars": num_vars}

                timeline = constructor.read_timeline(edgearray)

                return {"incidenceGraph": incidence_graph,
                        "generalGraph": False,
                        "tdTimeline": timeline,
                        "treeDecJson": tree_dec_json}

    except (Exception, pg.DatabaseError) as error:
        LOGGER.error(error)
        raise error
    return {}


if __name__ == "__main__":
    LOGGER.setLevel(logging.DEBUG)

    RESULTJSON = create_json(problem=10)
    with open('dbjson.json', 'w') as outfile:
        json.dump(RESULTJSON, outfile, sort_keys=True, indent=2,
                  ensure_ascii=False)
        LOGGER.info("Wrote to %s", outfile)
