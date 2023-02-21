from typing import Dict, List, Union

from pydantic import BaseModel, validator


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
    director: List[str]
    actors_names: List[str]
    actors: List[Dict]
    writers_names: List[str]
    writers: List[Dict]