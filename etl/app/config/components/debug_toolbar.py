import os
from pathlib import Path

from dotenv import load_dotenv

# корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# загрузка переенных окружения
load_dotenv(BASE_DIR / ".env")

mask = bool(int(os.getenv("DEBUG")))
if mask:

    def show_toolbar(request):
        return True

else:

    def show_toolbar(request):
        return False


DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}
