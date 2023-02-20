"""Модуль с настройками django проекта."""

# импорт библиотек
import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

# корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# загрузка переенных окружения
load_dotenv(BASE_DIR / ".env")
# секрет джанго
SECRET_KEY = os.getenv("SECRET_KEY")
# режим запуска
DEBUG = bool(int(os.getenv("DEBUG")))
# доступные порты в режиме деплоя (DEBUG=False)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
# для панели дебага
INTERNAL_IPS = os.getenv("INTERNAL_IPS").split(",")
# контроллеры
ROOT_URLCONF = "config.urls"
# вебсервер
WSGI_APPLICATION = "config.wsgi.application"
# язык
LANGUAGE_CODE = "en-EN"
# директория со стотическими файлами
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# директория с локализацией
LOCALE_PATHS = ["movies/locale"]

# компоненты, выведенные в отдельный модуль
include(
    "components/databases.py",
    "components/installed_apps.py",
    "components/middleware.py",
    "components/templates.py",
    "components/auth_password_validators.py",
    "components/time.py",
    "components/restframework.py",
    "components/logging.py",
    "components/debug_toolbar.py",
)
