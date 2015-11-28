from django.db import models
from django.contrib.auth.models import User

class Mreza(models.Model):
    ime = models.CharField(max_length=30)
    datum = models.DateTimeField()
    sirina = models.IntegerField()
    visina = models.IntegerField()
    aktivna = models.BooleanField()
    uporabnik = models.ForeignKey(User)

class Batiment(models.Model):
    visina_bat = models.IntegerField()
    sirina_bat = models.IntegerField()
    vrsta = models.CharField(max_length=30)
    ime = models.CharField(max_length=20)
    mreza = models.ForeignKey(Mreza)
    
class Koordinate(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    aktivna = models.BooleanField()
    batiment = models.ForeignKey(Batiment)

#class Zgodovina(models.Model):
#    premik = models.ForeignKey    