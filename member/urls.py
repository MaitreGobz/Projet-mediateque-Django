from django.urls import path, include
from . import views

app_name = 'member'
urlpatterns = [
    path("medias/", views.medias_list, name="medias_list"),
]