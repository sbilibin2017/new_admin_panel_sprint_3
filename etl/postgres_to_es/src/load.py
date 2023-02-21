from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from utils.logger import logger
from utils.state import State


def load(data: List[Dict], es_conn: Elasticsearch, state: State, l_updated_at: list) -> None:
    # корень проекта
    BASE_DIR = Path(__file__).resolve().parent.parent
    # загрузка переенных окружения
    load_dotenv(BASE_DIR / '.env.dev')
    for row, new_updated_at in zip(data, l_updated_at):
        es_conn.index(index='movies', doc_type="_doc", id=row['id'], body=row)
        state.set_state('updated_at', new_updated_at)
        logger.info(f'New updatet_at: {new_updated_at} ...')
