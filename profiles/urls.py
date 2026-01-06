from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
    path("search/", views.profile_search, name="search"),
    path("<int:pk>/followers/", views.profile_followers, name="followers"),
    path("<int:pk>/following/", views.profile_following, name="following"),
    path("<int:pk>/", views.profile_detail, name="detail"),
    path("edit/", views.profile_edit, name="edit"),
]
