REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "movies.api.v1.paginators.MoviesViewSetPaginator",
    "PAGE_SIZE": 50,
}
