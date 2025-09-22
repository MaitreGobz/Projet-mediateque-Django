from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Livre, Dvd, Cd, JeuDePlateau


@login_required(login_url="accounts:login")
def medias_list(request):
    ctx = {
        "livres": Livre.objects.order_by("titre"),
        "dvds": Dvd.objects.order_by("titre"),
        "cds": Cd.objects.order_by("titre"),
        "jeudeplateaus": JeuDePlateau.objects.order_by("titre"),
    }
    return render(request, "member/medias_list.html", ctx)