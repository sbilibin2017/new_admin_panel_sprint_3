import sys
import time
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

from src.extract import extract
from src.load import load
from src.transform import transform
from utils.db_connections import get_min_max_state, setup_connections
from utils.logger import logger


def main():
    # project root
    BASE_DIR = Path(__file__).resolve().parent
    PATH_TO_ENV = BASE_DIR / '.env.dev'
    # load env variables
    load_dotenv(PATH_TO_ENV)

    postgres_dict, es_conn, state = setup_connections()
    min_state, max_state = get_min_max_state(postgres_dict)
    current_state = state.get_state('updated_at')
    if current_state is None:
        state.set_state('updated_at', max_state)
        current_state = state.get_state('updated_at')
        return current_state, min_state
    elif current_state != min_state:
        try:
            with psycopg2.connect(**postgres_dict) as postgres_conn:
                df, df_fwg, df_fwp = extract(postgres_conn, current_state)
                data, l_updated_at = transform(df, df_fwg, df_fwp)
                load(data, es_conn, state, l_updated_at)
                return current_state, min_state
        except psycopg2.OperationalError:
            logger.info('cant connect to postgres ...')
            sys.exit(1)


if __name__ == '__main__':
    SLEEP = 5
    while True:
        main()
        time.sleep(SLEEP)
