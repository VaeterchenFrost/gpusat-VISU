"""
@author Martin Röbke
Created on Tue Mar 31 18:49:00 2020

See https://www.postgresqltutorial.com/postgresql-python/connect/
and reference
https://github.com/VaeterchenFrost/dp_on_dbs.git
"""
import psycopg2 as pg
import itertools
import json
from more_itertools import locate

from dijkstra import bidirectional_dijkstra as find_path, convert_to_adj


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
    return (
        num_vars,
        num_clauses,
        model_count,
        name,
        ptype,
        num_bags,
        tree_width,
        setup_start_time,
        calc_start_time,
        end_time)


def read_clauses(cursor, problem):
    """Return the clauses used for satiyfiability.
    Variables are counted from 1 and negative if negated in the clause.
    For example:
        "clausesJson" :
        [
        {
            "id" : 1,
            "list" : [ 1, -4, 6 ]
        },...]
    """
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
    # check bag numbering:
    cursor.execute(
        "SELECT bag FROM public.p{}_td_bag group by bag".format(problem))
    bags = sorted(list(flatten(cursor.fetchall())))
    print("bags:", bags)
    for bag in bags:
        cursor.execute(
            "SELECT node FROM public.p{}_td_bag WHERE bag={}".format(
                problem, bag))
        result = list(flatten(cursor.fetchall()))
        cursor.execute(
            "SELECT start_time,end_time-start_time "
            "FROM public.p{}_td_node_status WHERE node={}".format(
                problem, bag))
        start_time, dtime = cursor.fetchone()
        labeldict.append(
            {"id": bag, "items": result, "labels":
             [str(result),
              start_time.strftime("%D %T"),
              "dtime=%.4fs" % dtime.total_seconds()]})
    return labeldict


def readTimeline(cursor, problem, edgearray):
    """
    Read from td_node_status and the edearray to
    - create the timeline of the solving process
    - construct the path and solution-tables used during solving.

    Parameters
    ----------
    cursor : psycopg2.cursor
        database cursor
    problem : int
        index of the problem.
    edgearray : array of pairs of bagids
        Representing the tree-like structure between all bag-ids.
        It is assumed that all ids are included in this array.
        Example: [(2, 1), (3, 2), (4, 2), (5, 4)]

    Returns
    -------
    result : array
        array of bagids and eventually solution-tables.

    """
    timeline = list()
    adj = convert_to_adj(edgearray)
    cursor.execute(
        "SELECT node FROM public.p{}_td_node_status".format(problem))
    order_solved = list(flatten(cursor.fetchall()))
    last = order_solved[-1]  # tour sol -> through result nodes along the edges
    startpath = find_path(adj, last, order_solved[0])
    timeline = [[bag] for bag in startpath[1]]
    # add the other bags in order_solved to the timeline
    last = order_solved[0]
    for bag in order_solved:
        path = find_path(adj, last, bag)
        for intermed in path[1][1:]:
            timeline.append([intermed])
        # query column names
        cursor.execute(
            "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_NAME = 'p{}_td_node_{}'".format(problem, bag))
        column_names = list(flatten(cursor.fetchall()))
        print('column_names', column_names)
        # get solutions
        cursor.execute(
            "SELECT * FROM public.p{}_td_node_{}".format(problem, bag))
        solution_raw = cursor.fetchall()
        print('solution_raw', solution_raw)
        # check for nulled variables - assuming whole columns are nulled:
        columns_notnull = [column_names[i] for i, x in
                           enumerate(solution_raw[0]) if x is not None]
        solution = [bag,
                    [[columns_notnull,
                     *list(map(lambda row: [int(v) for v in row if v is not None],
                               solution_raw))],
                        "sol bag " + str(bag),
                        "sum: " + str(sum([li[-1] for li in solution_raw])),
                        True]]
        timeline.append(solution)
        last = bag

    return timeline


def read_edgearray(cursor, problem):
    cursor.execute(
        "SELECT node,parent FROM public.p{}_td_edge".format(problem))
    result = cursor.fetchall()
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

        timeline = readTimeline(cur, problem, edgearray)
        return {"clausesJson": clausesJson,
                "tdTimeline": timeline,
                "treeDecJson": treeDecJson}
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

    except (Exception, pg.DatabaseError) as error:
        print(error)

    return conn


if __name__ == "__main__":
    db = connect()
    resultjson = create_json(db, problem=5)
    with open('dbjson.json', 'w') as outfile:
        json.dump(resultjson, outfile,sort_keys = True, indent = 2,
               ensure_ascii = False)
