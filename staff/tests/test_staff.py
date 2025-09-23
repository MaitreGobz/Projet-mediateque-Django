from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Emprunteur, Livre, Emprunt

User = get_user_model()

class StaffViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff  = User.objects.create_user(username="biblio", password="test1234", is_staff=True)
        cls.member = User.objects.create_user(username="membre", password="test1234", is_staff=False)
        cls.emprunteur = Emprunteur.objects.create(nom="Bob")
        cls.livre = Livre.objects.create(titre="Livre Staff", auteur="AA", disponible=True)

    def test_staff_pages_require_staff(self):
        url = reverse("staff:media_list_staff")
        # non connecté -> redirection login staff
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/staff/login", resp["Location"])
        # connecté non-staff -> toujours redirigé
        self.client.login(username="membre", password="test1234")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.client.logout()
        # staff -> 200
        self.client.login(username="biblio", password="test1234")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_creer_emprunt(self):
        self.client.login(username="biblio", password="test1234")
        url = reverse("staff:emprunt_add")
        data = {
            "emprunteur": self.emprunteur.id,
            "livre": self.livre.id,
            "dvd": "",
            "cd": "",
        }
        resp = self.client.post(url, data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.livre.refresh_from_db()
        self.assertFalse(self.livre.disponible)
        self.assertEqual(Emprunt.objects.count(), 1)

    def test_marquer_retour(self):
        e = Emprunt.objects.create(emprunteur=self.emprunteur, livre=self.livre)
        self.assertFalse(self.livre.disponible)
        self.client.login(username="biblio", password="test1234")
        url = reverse("staff:emprunt_retour", kwargs={"pk": e.pk})  # adapte si besoin
        resp = self.client.get(url, follow=True)  # ta vue de retour est en GET
        self.assertEqual(resp.status_code, 200)
        self.livre.refresh_from_db()
        e.refresh_from_db()
        self.assertTrue(self.livre.disponible)
        self.assertIsNotNone(e.date_retour)