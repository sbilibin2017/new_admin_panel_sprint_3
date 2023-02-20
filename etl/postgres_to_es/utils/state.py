import abc
import json
from datetime import date, datetime
from typing import Any, Optional


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище."""
        json_object = json.dumps(state, default=self.json_serial)
        with open(self.file_path, "w") as f:
            f.write(json_object)

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища."""
        try:
            with open(self.file_path, "r") as f:
                current_state = json.load(f)
            return current_state
        except Exception:
            return {}

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        state = {key: value}
        self.save_state(state)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу."""
        state = self.retrieve_state()
        try:
            return state[key]
        except Exception:
            return None
