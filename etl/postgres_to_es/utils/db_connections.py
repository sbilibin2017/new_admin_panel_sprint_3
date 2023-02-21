import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

import psycopg2
import redis
from elasticsearch import Elasticsearch
from psycopg2.extras import DictCursor

from utils.state import State
from utils.validators import PostgresConfig

# project root
BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_ENV = BASE_DIR / '.env.dev'


def get_postgres_dict():
    '''Get postgres params.'''
    postgres_dict = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
    }
    postgres_dict = PostgresConfig(
        host=postgres_dict['host'],
        port=postgres_dict['port'],
        dbname=postgres_dict['dbname'],
        user=postgres_dict['user'],
        password=postgres_dict['password'],
    ).dict()
    return postgres_dict


def get_es_instance():
    '''Get elasticsearch instance.'''
    return Elasticsearch([os.getenv('ES_DSL')], retry_on_timeout=True)


def setup_connections():
    '''
    Set connections to postgres, redis,
    elasticsearch, init state.
    '''
    # connection to postgres
    postgres_dict = get_postgres_dict()
    # connection to elasticsearch
    es_conn = get_es_instance()
    with open(BASE_DIR / os.getenv('MAPPING_FILENAME'), 'r') as f:
        mapping = json.load(f)
    indices = es_conn.indices.get_alias().keys()
    if 'movies' not in indices:
        print('CREATING----------------')
        es_conn.indices.create(index='movies', ignore=400, body=mapping)
    es_conn.indices.get_mapping('movies')
    client = redis.Redis(host='cache', port=6379, db=0)
    state = State(client)
    return postgres_dict, es_conn, state


def get_min_max_state(postgres_dict: Dict) -> Tuple[datetime]:
    '''Get min and max date from postgres.'''
    with psycopg2.connect(**postgres_dict) as postgres_conn:
        with postgres_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""SELECT min(updated_at) FROM filmwork""")
            min_state = cursor.fetchall()[0][0]
            cursor.execute("""SELECT max(updated_at) FROM filmwork""")
            max_state = cursor.fetchall()[0][0]
            return min_state, max_state
