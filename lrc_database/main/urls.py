from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("users/<int:user_id>", views.user_profile, name="user_profile"),
    path("users/<int:user_id>/edit", views.edit_profile, name="edit_profile"),
    path("users/<str:group>", views.list_users, name="list_users"),
]
