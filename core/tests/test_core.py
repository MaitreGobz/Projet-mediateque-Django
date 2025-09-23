from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from core.models import Emprunteur, Livre, Dvd, Cd, JeuDePlateau, Emprunt

class BusinessRulesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.emprunteur = Emprunteur.objects.create(nom="Alice")
        cls.livre = Livre.objects.create(titre="Livre A", auteur="Aut A", disponible=True)
        cls.dvd   = Dvd.objects.create(titre="DVD A", realisateur="Real A", disponible=True)
        cls.cd    = Cd.objects.create(titre="CD A", artiste="Art A", disponible=True)
        cls.livre2    = Livre.objects.create(titre="Livre B", auteur="Aut B", disponible=True)
        cls.livre3    = Livre.objects.create(titre="Livre C", auteur="Aut C", disponible=True)
        cls.livre4    = Livre.objects.create(titre="Livre D", auteur="Aut D", disponible=True)
        cls.jeu   = JeuDePlateau.objects.create(titre="Catan")  # non empruntable par construction

    def test_emprunt_succes_rend_media_indisponible(self):
        e = Emprunt.objects.create(emprunteur=self.emprunteur, livre=self.livre)
        self.livre.refresh_from_db()
        self.assertFalse(self.livre.disponible)
        self.assertIsNone(e.date_retour)

    def test_limite_3_emprunts(self):
        Emprunt.objects.create(emprunteur=self.emprunteur, livre=self.livre)
        Emprunt.objects.create(emprunteur=self.emprunteur, dvd=self.dvd)
        Emprunt.objects.create(emprunteur=self.emprunteur, cd=self.cd)
        with self.assertRaises(ValidationError):
            Emprunt.objects.create(emprunteur=self.emprunteur, livre=self.livre2)

    def test_retard_bloque_emprunt(self):
        e = Emprunt.objects.create(emprunteur=self.emprunteur, livre=self.livre3)
        # force un retard
        Emprunt.objects.filter(pk=e.pk).update(
            date_emprunt=timezone.now() - Emprunt.DUREE - timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            Emprunt.objects.create(emprunteur=self.emprunteur, livre=self.livre4)

    def test_jeu_non_empruntable_par_construction(self):
        # pas de FK vers JeuDePlateau
        with self.assertRaises(TypeError):
            Emprunt.objects.create(emprunteur=self.emprunteur, jeu=self.jeu)

    def test_retour_rend_media_disponible(self):
        e = Emprunt.objects.create(emprunteur=self.emprunteur, livre=self.livre2)
        e.marquer_retour()
        self.livre2.refresh_from_db()
        e.refresh_from_db()
        self.assertIsNotNone(e.date_retour)
        self.assertTrue(self.livre2.disponible)

    def test_est_en_retard_calcule(self):
        e = Emprunt.objects.create(emprunteur=self.emprunteur, livre=self.livre3)
        self.assertFalse(e.est_en_retard)
        Emprunt.objects.filter(pk=e.pk).update(
            date_emprunt=timezone.now() - Emprunt.DUREE - timedelta(days=1)
        )
        e.refresh_from_db()
        self.assertTrue(e.est_en_retard)
