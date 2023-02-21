import sys
from typing import Dict, Tuple

import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
from utils.logger import logger


def get_filmwork_query(current_state):
    '''Creates filmwork query with respect of current etl state.'''
    filmwork_keys = 'id,rating,title,description,updated_at'
    query = f"""
                SELECT {filmwork_keys}
                FROM filmwork
                WHERE updated_at <= %s
                ORDER BY updated_at DESC
            """
    return query, current_state


def get_filmwork_4idxs(chunk):
    '''Creatres dataframe for filmwork.'''
    filmwork_colnames = ['id', 'rating', 'title', 'description', 'updated_at']
    df = pd.DataFrame.from_records(chunk, columns=filmwork_colnames)
    return df


def get_filmwork_genre_4idxs(cursor, df):
    '''Creatres dataframe for filmwork genres.'''
    keys = 'filmwork_id,genre_id,name,description'
    colnames = keys.split(',')
    filwork_idxs = tuple(df['id'].values.tolist())
    wc = ','.join(['%s' for _ in range(len(filwork_idxs))])
    query = f"""
                SELECT {keys}
                FROM filmwork_genre fwg
                LEFT JOIN genre g
                    ON fwg.genre_id = g.id
                WHERE filmwork_id in ({wc})
            """
    cursor.execute(query, filwork_idxs)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=colnames).rename(columns={'filmwork_id': 'id'})
    return df


def get_filmwork_person_4idxs(cursor, df):
    '''Creatres dataframe for filmwork persons.'''
    keys = 'filmwork_id,person_id,full_name,role'
    colnames = keys.split(',')
    filwork_idxs = tuple(df['id'].values.tolist())
    wc = ','.join(['%s' for _ in range(len(filwork_idxs))])
    query = f"""
                SELECT {keys}
                FROM filmwork_person fwp
                    LEFT JOIN person p
                    ON fwp.person_id = p.id
                WHERE filmwork_id in ({wc})
            """
    cursor.execute(query, filwork_idxs)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=colnames).rename(
        columns={'full_name': 'name', 'filmwork_id': 'id'}
    )
    return df


def get_dataframes(cursor, chunk):
    df = get_filmwork_4idxs(chunk)
    # dataframe with filmwork and genres
    df_fwg = get_filmwork_genre_4idxs(cursor, df)
    # dataframe with filmwork and persons
    df_fwp = get_filmwork_person_4idxs(cursor, df)
    return df, df_fwg, df_fwp


CHUNK_SIZE = 1000


def extract(postgres_conn, current_state) -> Tuple[Dict]:
    '''Extracts data from postgres.'''    
    # query for current state and filmworks
    logger.info('getting current state ...')
    query, current_state = get_filmwork_query(current_state)
    try:
        # connecting to postgres
        logger.info('connecting to postgre ...')
        with postgres_conn.cursor(cursor_factory=DictCursor) as cursor:
            logger.info('\t[connected] executing query ...')            
            cursor.execute(query, (current_state,))
            chunk = cursor.fetchmany(CHUNK_SIZE)
            # dataframes
            logger.info('\t[connected] preparing dataframes ...')
            df, df_fwg, df_fwp = get_dataframes(cursor, chunk)
            return df, df_fwg, df_fwp
    except psycopg2.OperationalError:
        logger.info('cant connect to postgres ...')
        sys.exit(1)
