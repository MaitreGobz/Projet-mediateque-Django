from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

class MemberLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = False


    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("member:medias_list")


class StaffLoginView(LoginView):
    template_name = "accounts/staff_login.html"
    redirect_authenticated_user = False

    def form_valid(self, form):
        """Refuse l’accès si l’utilisateur n’est pas staff."""
        user = form.get_user()
        if not user.is_staff:
            messages.error(self.request, "Accès réservé au personnel.")
            return redirect("accounts:login")
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("staff:home")
