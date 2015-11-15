from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Mreza(models.Model):
    sirina = models.IntegerField()
    visina = models.IntegerField()
    uporanbik = models.ForeignKey(User)

class Batiment(models.Model):
    visina_bat = models.IntegerField()
    sirina_bat = models.IntegerField()
    vrsta = models.CharField(max_length=30)
    ime = models.CharField(max_length=20)
    pozX = models.IntegerField()
    pozY = models.IntegerField()
    