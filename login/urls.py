from django.urls import path
from login import views


urlpatterns = [
    path("create_user/", views.create_user, name="create_user"),
    path("", views.login, name="login"),
]

