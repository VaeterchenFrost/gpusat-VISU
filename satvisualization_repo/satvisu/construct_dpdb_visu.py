"""
@author Martin Röbke
Created on Tue Mar 31 18:49:00 2020
"""
import psycopg2 as pg

def read_cfg(cfg_file):
    # import json

    # with open(cfg_file) as c:
    #     cfg = json.load(c)
    cfg = {'postgresql':{
        "host": "localhost",
        "port": 5432,
        "database": "logicsem",
        "user": "postgres",
        "password": "pr|fd=/`66{+s`Bp",
        "application_name": "dpdb-admin"
        }}
    return cfg


# https://www.postgresqltutorial.com/postgresql-python/connect/

def config(filename='database.ini', section='postgresql'):
 
    cfg = read_cfg(filename)
    if section in cfg:
        db = cfg[section]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db

        
if __name__ == "__main__":
    params=config()
    print(params)
    _db_name = params["database"]
    _conn = pg.connect(**params)
    print("connected to", _db_name)
    