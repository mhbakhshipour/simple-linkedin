from django.urls import path

from . import views

app_name = "relationships"

urlpatterns = [
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("<int:pk>/unfollow/", views.unfollow, name="unfollow"),
]

