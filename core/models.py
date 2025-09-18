from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

# Médias

class Media(models.Model):

    """Base commune pour les médias empruntables (Livre/Dvd/Cd)."""

    class Meta:
        abstract = True

    titre = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre


class Livre(Media):
    auteur = models.CharField(max_length=200)


class Dvd(Media):
    realisateur = models.CharField(max_length=200)


class Cd(Media):
    artiste = models.CharField(max_length=200)


class JeuDePlateau(models.Model):
    """Consultable uniquement"""
    titre = models.CharField(max_length=200)
    createur = models.CharField(max_length=200)

    def __str__(self):
        return self.titre

# Membres

class Emprunteur(models.Model):
    nom = models.CharField(max_length=200)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

    def emprunts_en_cours(self):
        return self.emprunt_set.filter(date_retour__isnull=True).count()

    def a_un_retard(self):
        return self.emprunt_set.filter(date_retour__isnull=True,
                                       date_emprunt__lte=timezone.now() - Emprunt.DUREE).exists()

    def est_bloque(self):
        return self.bloque or self.a_un_retard()

# Emprunts

class Emprunt(models.Model):

    """1 emprunt relie un emprunteur à un média Livre ou Cd ou Dvd"""

    DUREE = timedelta(days=7)

    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE)

    #FK pour renseigner un emprunt

    livre = models.ForeignKey(Livre, null=True, blank=True, on_delete=models.PROTECT)
    dvd = models.ForeignKey(Dvd, null=True, blank=True, on_delete=models.PROTECT)
    cd = models.ForeignKey(Cd, null=True, blank=True, on_delete=models.PROTECT)

    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        media = self.media_object()
        return f"{self.emprunteur} ({self.date_emprunt})"

    def media_object(self):

        """Retourne l'objet média emprunté"""

        return self.livre or self.dvd or self.cd

    @property
    def est_en_retard(self):
        if self.date_retour:
            return False
        return timezone.now() > self.date_emprunt + self.DUREE

    def clean(self):

        """Validation des règles métier dans le modèle"""

        super().clean()

        # 1 seul média emprunter lors d'un emprunt

        medias = [self.livre, self.dvd, self.cd]
        if sum(m is not none for m in medias) != 1:
            raise ValidationError("Un emprunt doit concerner un seul média.")

        #Jeu de plateau non empruntable comme défini dans le modèle

        #L'emprunteur ne doit pas être bloqué

        if self.emprunteur and self.emprunteur.est_bloque():
            raise ValidationError("Le membre est bloqué à cause d'un retard.")

        #Limite de 3 emprunts  en cours par membre

        en_cours = self.emprunteur.emprunts_en_cours() if self.emprunteur_id else 0
        if self._state.adding and en_cours >=3 :
            raise ValidationError("Limite de 3 emprunts atteinte pour ce membre.")

        #Média doit être disponible

        media = self.media_object()
        if media and not media.disponible:
            raise ValidationError("Le média n'est pas disponible.")


    def save(self, *args, **kwargs):

        """
        On force la validation (full_clean) et on met à jour la disponibilité du média.
        """

        self.full_clean()

        with transaction.atomic():
            super().save(*args, **kwargs)
            # Marquer le média indisponible si l'emprunt vient d'être créé
            if self.date_retour is None:
                media = self.media_object()
                if media and media.disponible:
                    media.disponible = False
                    media.save(update_fields=["disponible"])

    # Action métier

    def marquer_retour(self):
        """
        Enregistre le retour du média : date_retour + disponibilité.
        """
        if self.date_retour is not None:
            return  # déjà retourné

        with transaction.atomic():
            self.date_retour = timezone.now()
            self.save(update_fields=["date_retour"])

            media = self.media_obj()
            if media:
                media.disponible = True
                media.save(update_fields=["disponible"])