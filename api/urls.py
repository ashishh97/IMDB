from django.urls import path
from api import views


urlpatterns = [
    path("add_movies/", views.add_movies, name="add_movies"),
    path("delete_movies/", views.delete_movies, name="delete_movies"),
    path("edit_movie/", views.edit_movie, name="edit_movie"),
    path("", views.search_movies, name="search_movies"),
]

