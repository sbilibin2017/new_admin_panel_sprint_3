from django.apps import AppConfig
from django.core.signals import request_finished
from django.utils.translation import gettext_lazy as _


class MoviesConfig(AppConfig):
    """App config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "movies"
    verbose_name = _("movies")

    def ready(self):
        from movies.api import signals

        request_finished.connect(signals.attention)
