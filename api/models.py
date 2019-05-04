from django.db import models
from datetime import datetime 

# Create your models here.

class Etat(models.Model):
    crise = models.IntegerField(default=0)
    date_reponse = models.DateTimeField(default=datetime.now, blank=True)
    
