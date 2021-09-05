from django.urls import path
from . import views
appname = "shortener"

urlpatterns = [
    path("", views.home_view, name = "Home"),
    path("<str:shortened_part>/", views.redirect_view, name = "Redirect"),
    path("<str:shortened_part>/stats/", views.stats_view, name = "Stats"),
    path("api/create/", views.create_endpoint, name = "Creating URL"),
    path("api/vanity/", views.vanity_create_endpoint, name = "Creating Vanity URL"),
    path("api/stats/<str:shortened_part>/", views.stats_endpoint, name = "Stats API"),
    path("api/all/", views.list_all_endpoint, name = "All URLs"),
    path("api/", views.api_root_endpoint, name = "API Root URL")
]