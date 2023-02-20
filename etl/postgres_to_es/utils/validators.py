from typing import Dict, List

from pydantic import BaseModel


class PostgresConfig(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: int


class PreparedData(BaseModel):
    id: str
    imdb_rating: float
    genre: List[str]
    title: str
    description: str
    actors_names: str
    actors: List[Dict]
    writers_names: str
    writers: List[Dict]
