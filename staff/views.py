from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Emprunteur, Livre, Dvd, Cd, JeuDePlateau, Emprunt
from django.utils import timezone

#Accueil staff
@staff_member_required(login_url="accounts:staff_login")
def home_staff(request):
    return render(request, "staff/home_staff.html")


#Membres
@staff_member_required(login_url="accounts:staff_login")
def emprunteur_list(request):
    emprunteurs = Emprunteur.objects.all()
    return render(request, "staff/emprunteur_list.html", {"emprunteurs": emprunteurs})

@staff_member_required(login_url="accounts:staff_login")
def emprunteur_add(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        Emprunteur.objects.create(nom=nom)
        return redirect("staff:emprunteur_list")
    return render(request, "staff/emprunteur_form.html", {"titre": "Ajouter un emprunteur"})

@staff_member_required(login_url="accounts:staff_login")
def emprunteur_edit(request, pk):
    edit = get_object_or_404(Emprunteur, pk=pk)
    if request.method == "POST":
        edit.nom = (request.POST.get("nom") or "").strip()
        edit.bloque = bool(request.POST.get("bloque"))
        edit.save()
        return redirect("staff:emprunteur_list")
    return render(request, "staff/emprunteur_form.html", {"titre": "Modifier un emprunteur", "emprunteur": edit})

@staff_member_required(login_url="accounts:staff_login")
def emprunteur_delete(request, pk):
    emprunteur = get_object_or_404(Emprunteur, pk=pk)
    if request.method == "POST":
        emprunteur.delete()
        return redirect("staff:emprunteur_list")
    return render(request, "staff/emprunteur_confirm_delete.html", {"emprunteur": emprunteur})


#Médias
@staff_member_required(login_url="accounts:staff_login")
def media_list_staff(request):
    ctx = {
        "livres": Livre.objects.order_by("titre"),
        "dvds": Dvd.objects.order_by("titre"),
        "cds": Cd.objects.order_by("titre"),
        "jeudeplateaus": JeuDePlateau.objects.order_by("titre"),
    }
    return render(request, "staff/media_list_staff.html", ctx)

@staff_member_required(login_url="accounts:staff_login")
def media_add_livre(request):
    if request.method == "POST":
        Livre.objects.create(
            titre=request.POST.get("titre"),
            auteur=request.POST.get("auteur")
        )
        return redirect("staff:media_list_staff")
    return render(request, "staff/media_form.html", {"titre": "Ajouter un livre", "type": "livre"})

@staff_member_required(login_url="accounts:staff_login")
def media_add_dvd(request):
    if request.method == "POST":
        Dvd.objects.create(
            titre=request.POST.get("titre"),
            realisateur=request.POST.get("realisateur")
        )
        return redirect("staff:media_list_staff")
    return render(request, "staff/media_form.html", {"titre": "Ajouter un DVD", "type": "dvd"})


@staff_member_required(login_url="accounts:staff_login")
def media_add_cd(request):
    if request.method == "POST":
        Cd.objects.create(
            titre=request.POST.get("titre"),
            artiste=request.POST.get("artiste")
        )
        return redirect("staff:media_list_staff")
    return render(request, "staff/media_form.html", {"titre": "Ajouter un CD", "type": "cd"})


@staff_member_required(login_url="accounts:staff_login")
def media_add_jeu(request):
    if request.method == "POST":
        JeuDePlateau.objects.create(
            titre=request.POST.get("titre"),
            createur=request.POST.get("createur")
        )
        return redirect("staff:media_list_staff")
    return render(request, "staff/media_form.html", {"titre": "Ajouter un Jeu de plateau", "type": "jeu"})


# Emprunts
@staff_member_required(login_url="accounts:staff_login")
def emprunt_list(request):
    emprunts = Emprunt.objects.all().order_by("date_emprunt")
    return render(request, "staff/emprunt_list.html", {"emprunts": emprunts})

@staff_member_required(login_url="accounts:staff_login")
def emprunt_add(request):
    if request.method == "POST":
        emprunteur_id = request.POST.get("emprunteur")
        livre_id = request.POST.get("livre")
        dvd_id   = request.POST.get("dvd")
        cd_id    = request.POST.get("cd")

        emprunteur = Emprunteur.objects.get(pk=emprunteur_id)
        livre = Livre.objects.filter(pk=livre_id).first() if livre_id else None
        dvd   = Dvd.objects.filter(pk=dvd_id).first() if dvd_id else None
        cd    = Cd.objects.filter(pk=cd_id).first() if cd_id else None

        Emprunt.objects.create(emprunteur=emprunteur, livre=livre, dvd=dvd, cd=cd)
        return redirect("staff:emprunt_list")

    ctx = {
        "titre": "Nouvel emprunt",
        "emprunteurs": Emprunteur.objects.order_by("nom"),
        "livres": Livre.objects.filter(disponible=True).order_by("titre"),
        "dvds": Dvd.objects.filter(disponible=True).order_by("titre"),
        "cds": Cd.objects.filter(disponible=True).order_by("titre"),
    }

    return render(request, "staff/emprunt_form.html", ctx)

@staff_member_required(login_url="accounts:staff_login")
def emprunt_retour(request, pk):
    emprunt = get_object_or_404(Emprunt, pk=pk)
    emprunt.marquer_retour()
    return redirect("staff:emprunt_list")
