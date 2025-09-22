from django.urls import path
from .views import MemberLoginView, StaffLoginView
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("login/", MemberLoginView.as_view(), name="login"),
    path("staff/login/", StaffLoginView.as_view(), name="staff_login"),
    path("logout/", LogoutView.as_view(next_page="core:home"), name="logout"),
]
