"""Django admin panel."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from movies.models import Filmwork, FilmworkGenre, FilmworkPerson, Genre, Person


def custom_titled_filter(title):
    """Name filter."""

    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


# Жанр
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Add genre to admin panel."""

    list_display = ("name", "description", "updated_at")


# Персона
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Add person to admin panel."""

    list_display = ("full_name", "updated_at")


# Кинопроизведение
class FilmworkGenreInline(admin.TabularInline):
    """Add filmwork genres to admin panel."""

    model = FilmworkGenre


class FilmworkPersonInline(admin.TabularInline):
    """Add filmwork persons to admin panel."""

    model = FilmworkPerson


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Add filmwork to admin panel."""

    # отображение жанров и персона в кинопроизведении
    inlines = (FilmworkGenreInline, FilmworkPersonInline)
    # Отображение полей в списке
    list_display = ("title", "description", "type", "rating", "creation_date")
    # # фильтры
    list_filter = ("type", ("genres__name", custom_titled_filter(_("Genre"))))
    # поиск
    search_fields = ("title", "description", "id", "persons__full_name")
