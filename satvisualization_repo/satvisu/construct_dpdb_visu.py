"""
@author Martin Röbke
Created on Tue Mar 31 18:49:00 2020

See https://www.postgresqltutorial.com/postgresql-python/connect/
and reference
https://github.com/VaeterchenFrost/dp_on_dbs.git
"""
import psycopg2 as pg
from more_itertools import locate
import itertools


def flatten(iterable):
    """ Flatten at first level.

    Turn ex=[[1,2],[3,4]] into
    [1, 2, 3, 4]
    and [ex,ex] into
    [[1, 2], [3, 4], [1, 2], [3, 4]]
    """
    return itertools.chain.from_iterable(iterable)


def read_cfg(cfg_file):
    """TODO: Read file"""

    cfg = {'postgresql': {
        "host": "localhost",
        "port": 5432,
        "database": "logicsem",
        "user": "postgres",
        "password": "pr|fd=/`66{+s`Bp",
        "application_name": "dpdb-admin"
    }}
    return cfg


def config(filename='database.ini', section='postgresql'):
    """Return the database config as JSON"""
    cfg = read_cfg(filename)
    if section in cfg:
        db = cfg[section]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(
                section, filename))

    return db


def read_problem(cursor, problem):
    cursor.execute("SELECT num_vars,num_clauses,model_count FROM "
                   "public.problem_sharpsat WHERE id={}".format(problem))
    num_vars, num_clauses, model_count = cursor.fetchone()
    cursor.execute("SELECT name,type,num_bags,tree_width,"
                   "setup_start_time,calc_start_time,end_time FROM "
                   "public.problem WHERE id={}".format(problem))
    (name, ptype, num_bags, tree_width,
     setup_start_time, calc_start_time, end_time) = cursor.fetchone()
    return (num_vars, num_clauses, model_count, name, ptype, num_bags, tree_width,
            setup_start_time, calc_start_time, end_time)


def read_clauses(cursor, problem):
    cursor.execute("SELECT * FROM public.p{}_sat_clause".format(problem))
    result = cursor.fetchall()
    result_cleaned = list(map(lambda x: [i + 1 if x[i] else -(i + 1) for i in
                                         locate(x, lambda p:p is not None)],
                              result))
    clausesJson = [{"id": i, "list": item}
                   for (i, item) in enumerate(result_cleaned, 1)]
    return clausesJson


def read_labeldict(cursor, problem, num_bags=1):
    labeldict = []
    for bag in range(num_bags):
        cursor.execute(
            "SELECT node FROM public.p{}_td_bag WHERE bag={}".format(
                problem, bag + 1))                  # one based in db
        result = list(flatten(cursor.fetchall()))
        labeldict.append(
            {"id": bag, "items": result, "labels": str(result)})
    return labeldict


def read_edgearray(cursor, problem):
    cursor.execute(
        "SELECT node,parent FROM public.p{}_td_edge".format(problem))
    result = cursor.fetchall()
    result = [[x - 1 for x in l] for l in result]     # zero based
    return result


def create_json(db, problem=1):
    result = {}

    try:
        # create a cursor
        cur = db.cursor()
        # create clausesJson
        clausesJson = read_clauses(cur, problem)

        (num_vars, num_clauses, model_count, name, ptype, num_bags, tree_width,
            setup_start_time, calc_start_time, end_time) = read_problem(cur, problem)
        # create treeDecJson
        labeldict = read_labeldict(cur, problem, num_bags)
        edgearray = read_edgearray(cur, problem)
        treeDecJson = {
            "bagpre": "bag %s",
            "edgearray": edgearray,
            "labeldict": labeldict,
            "numVars": num_vars}
    except (Exception, pg.DatabaseError) as error:
        print(error)


def connect():
    """ Connect to the PostgreSQL database server using the params from config"""
    conn = None
    try:
        # read connection parameters
        params = config()
        db_name = params["database"]

        print(
            "Connecting to the PostgreSQL database",
            "'" + db_name + "'",
            "...")
        conn = pg.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # display the PostgreSQL database server version
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
        create_json(conn, 5)

    except (Exception, pg.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == "__main__":
    connect()
