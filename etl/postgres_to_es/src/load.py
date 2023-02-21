import time
from pathlib import Path

from dotenv import load_dotenv
from utils.logger import logger


def load(data, es_conn, state, l_updated_at):
    # корень проекта
    BASE_DIR = Path(__file__).resolve().parent.parent
    # загрузка переенных окружения
    load_dotenv(BASE_DIR / '.env.dev')
    for row, new_updated_at in zip(data, l_updated_at):
        es_conn.index(index='movies', doc_type="_doc", id=row['id'], body=row)
        state.set_state('updated_at', new_updated_at)        
        logger.info(f'New updatet_at: {new_updated_at} ...')
