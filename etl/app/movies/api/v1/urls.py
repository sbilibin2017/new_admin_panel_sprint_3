"""DRF маршруты апи 1ой версии."""

from django.urls import include, path
from movies.api.v1 import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("movies", views.MoviesViewSet, basename="movies")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
]
