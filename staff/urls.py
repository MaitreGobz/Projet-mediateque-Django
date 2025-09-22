from django.urls import path
from . import views

app_name = "staff"
urlpatterns = [
    path("", views.home_staff, name="home"),

    # Emprunteurs
    path("emprunteurs/", views.emprunteur_list, name="emprunteur_list"),
    path("emprunteurs/ajouter/", views.emprunteur_add, name="emprunteur_add"),
    path("emprunteurs/<int:pk>/editer/", views.emprunteur_edit, name="emprunteur_edit"),
    path("emprunteurs/<int:pk>/supprimer/", views.emprunteur_delete, name="emprunteur_delete"),

    # Médias
    path("medias/", views.media_list_staff, name="media_list_staff"),
    path("medias/ajouter/livre/", views.media_add_livre, name="media_add_livre"),
    path("medias/ajouter/dvd/", views.media_add_dvd, name="media_add_dvd"),
    path("medias/ajouter/cd/", views.media_add_cd, name="media_add_cd"),
    path("medias/ajouter/jeu/", views.media_add_jeu, name="media_add_jeu"),

    # Emprunts
    path("emprunts/", views.emprunt_list, name="emprunt_list"),
    path("emprunts/ajouter/", views.emprunt_add, name="emprunt_add"),
    path("emprunts/<int:pk>/retour/", views.emprunt_retour, name="emprunt_retour"),
]