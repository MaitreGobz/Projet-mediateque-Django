from django.urls import path, include
from . import views

app_name = 'staff'
urlpatterns = [
    path("table/", views.home_staff, name="home_staff")
]