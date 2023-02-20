"""Views."""

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Q
from django.db.models.functions import Coalesce
from movies.api.v1.serializers import MoviesListSerializer
from movies.models import Filmwork
from rest_framework import viewsets


class MoviesViewSet(viewsets.ReadOnlyModelViewSet):
    """View for list of movies with info about genres and persons."""

    # django model
    model = Filmwork
    # drf serializer
    serializer_class = MoviesListSerializer

    def filter_role(self, role):
        """Filter person with role type."""
        return ArrayAgg(
            "persons__full_name",
            distinct=True,
            filter=Q(filmworkperson__role=role),
            default=[],
        )

    def get_queryset(self):
        """Build queryset."""
        queryset = (
            self.model.objects.prefetch_related("persons", "genres")
            .values("id", "title", "description", "creation_date", "type")
            .annotate(
                rating=Coalesce(F("rating"), 0.0),
                genres=ArrayAgg("genres__name", distinct=True, default=[]),
                actors=self.filter_role("actor"),
                directors=self.filter_role("director"),
                writers=self.filter_role("writer"),
            )
        )

        return queryset
