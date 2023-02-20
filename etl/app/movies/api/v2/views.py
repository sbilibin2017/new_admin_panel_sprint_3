from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Q
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesApiMixin:
    """Mixin for list and detailed views for movies."""

    model = Filmwork
    http_method_names = ["get"]

    def filter_role(self, role):
        """Filter person with role type."""
        return ArrayAgg(
            "persons__full_name",
            distinct=True,
            filter=Q(filmworkperson__role=role),
            default=[],
        )

    def add_genre_filter(self, queryset):
        genre = self.request.GET.get("genre")
        if genre is not None:
            queryset = queryset.filter(genres__contains=[genre])
        return queryset

    def add_title_filter(self, queryset):
        title = self.request.GET.get("title")
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    def get_queryset(self):
        """Build queryset."""
        queryset = self.model.objects.values("id", "title", "description", "creation_date", "type").annotate(
            rating=Coalesce(F("rating"), 0.0),
            genres=ArrayAgg("genres__name", distinct=True, default=[]),
            actors=self.filter_role("actor"),
            directors=self.filter_role("director"),
            writers=self.filter_role("writer"),
        )
        queryset = self.add_genre_filter(queryset)
        queryset = self.add_title_filter(queryset)

        return queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """List movies  view with info."""

    paginate_by = 50

    def prepare_context_data(self, paginator, page, queryset, is_paginated):
        """Prepare context data."""
        data = list(queryset)
        count = paginator.count
        total_pages = paginator.num_pages
        if is_paginated:
            next = page.next_page_number() if page.has_next() else None
            prev = page.previous_page_number() if page.has_previous() else None
        else:
            next = 2
            prev = None
        return {
            "count": count,
            "total_pages": total_pages,
            "prev": prev,
            "next": next,
            "results": data,
        }

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator, page, queryset, is_paginated = self.paginate_queryset(self.get_queryset(), self.paginate_by)
        context = self.prepare_context_data(paginator, page, queryset, is_paginated)
        return context


class MoviesDetailApi(MoviesApiMixin, DetailView):
    """One movie with info."""

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get("pk", "")
        context = list(super().get_queryset().filter(id=pk))[0]
        return context
