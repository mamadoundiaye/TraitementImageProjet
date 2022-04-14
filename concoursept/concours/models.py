from django.db import models

# Create your models here.
class Candidat(models.Model):
    class Meta:
        ordering = ("candidat_id",)
        pass

    def __str__(self):
        return self.prenom + " " + self.nom + " " + str(self.candidat_id)

    candidat_id = models.AutoField(primary_key=True)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    lycee = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    telephone = models.CharField(max_length=100)
    genie = models.CharField(max_length=100)
    centre = models.CharField(max_length=100)

    moy_seconde = models.FloatField(default=0)
    moy_premiere = models.FloatField(default=0)
    moy_terminale = models.FloatField(default=0)
    moy_bac = models.FloatField(default=0)
    moy_concours = models.FloatField(default=0)

    def get_moy_general(self):
        return (
            (self.moy_seconde + self.moy_premiere + self.moy_terminale) / 3
            + self.moy_bac
            + self.moy_concours
        ) / 3

    moy_general = property(get_moy_general)
