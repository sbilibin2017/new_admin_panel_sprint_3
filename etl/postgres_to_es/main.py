import sys
import time
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

from src.extract import extract
from src.load import load
from src.transform import transform
from utils.db_connections import setup_connections
from utils.logger import logger

SLEEP = 10


def main():
    # project root
    BASE_DIR = Path(__file__).resolve().parent
    PATH_TO_ENV = BASE_DIR / '.env.dev'
    # load env variables
    load_dotenv(PATH_TO_ENV)
    postgres_dict, es_conn, state = setup_connections()

    current_state = state.get_state('updated_at')
    with psycopg2.connect(**postgres_dict) as postgres_conn:
        with postgres_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""SELECT min(updated_at) FROM filmwork""")
            min_state = cursor.fetchall()[0][0]
            cursor.execute("""SELECT max(updated_at) FROM filmwork""")
            max_state = cursor.fetchall()[0][0]
    if current_state is None:
        state.set_state('updated_at', max_state)
        current_state = state.get_state('updated_at')
        return current_state, min_state
    elif current_state != min_state:
        try:
            with psycopg2.connect(**postgres_dict) as postgres_conn:
                try:
                    df, df_fwg, df_fwp = extract(postgres_conn, current_state)
                    data, l_updated_at = transform(df, df_fwg, df_fwp)
                    load(data, es_conn, state, l_updated_at)
                    return current_state, min_state
                except BaseException:
                    logger.info('There is no new records...')
                    return current_state, min_state
        except psycopg2.OperationalError:
            logger.info('cant connect to postgres ...')
            sys.exit(1)
    else:
        logger.info('There is no new records...')
        return current_state, min_state


if __name__ == '__main__':
    while True:
        current_state, min_state = main()
        print('############################')
        print(f'current_state:{current_state}, min_state:{min_state}')
        print('############################')
        if current_state == min_state:
            time.sleep(60)
        else:
            time.sleep(6)
