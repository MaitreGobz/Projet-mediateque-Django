from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Livre, Dvd, Cd, JeuDePlateau

User = get_user_model()

class PublicViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="membre1", password="test1234", is_staff=False)
        Livre.objects.create(titre="Livre Pub", auteur="X", disponible=True)
        Dvd.objects.create(titre="DVD Pub", realisateur="Y", disponible=True)
        Cd.objects.create(titre="CD Pub", artiste="Z", disponible=True)
        JeuDePlateau.objects.create(titre="Patchwork")

    def test_medias_list_requires_login(self):
        url = reverse("member:medias_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp["Location"])

    def test_medias_list_ok_and_contains_items(self):
        self.client.login(username="membre1", password="test1234")
        url = reverse("member:medias_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Livre Pub")
        self.assertContains(resp, "DVD Pub")
        self.assertContains(resp, "CD Pub")
        self.assertContains(resp, "Patchwork")