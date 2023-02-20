"""DRF сериализаторы апи 1ой версии."""


from movies.models import Filmwork
from rest_framework import serializers


class StringListField(serializers.ListField):
    """List field with strings."""

    child = serializers.CharField()


class MoviesListSerializer(serializers.ModelSerializer):
    """Serializer for movies with genres and persons info."""

    genres = StringListField()
    actors = StringListField()
    directors = StringListField()
    writers = StringListField()

    class Meta:
        model = Filmwork
        fields = [
            "id",
            "title",
            "description",
            "creation_date",
            "rating",
            "type",
            "genres",
            "actors",
            "directors",
            "writers",
        ]
