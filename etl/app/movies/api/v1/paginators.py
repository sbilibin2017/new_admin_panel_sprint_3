"""Pagination."""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MoviesViewSetPaginator(PageNumberPagination):
    """Drf paginator."""

    page = 1
    page_size = 50

    def get_paginated_response(self, data):
        data_resp = {
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "next": self.get_next_link(),
            "prev": self.get_previous_link(),
            "results": data,
        }
        return Response(data_resp)
