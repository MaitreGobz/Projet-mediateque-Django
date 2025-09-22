from django.urls import path
from . import views

app_name = "public"
urlpatterns = [
    path("medias/", views.medias_list, name="medias_list"),
]
