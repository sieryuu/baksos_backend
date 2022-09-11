from django.db import models

from common.models import CrudModel


# Create your models here.
class Puskesmas(CrudModel):
    puskesmas = models.CharField(max_length=30, primary_key=True)
    pulau = models.CharField(max_length=30)

class Penyakit(CrudModel):
    nama = models.CharField(max_length=10, primary_key=True)
    grup = models.CharField(max_length=20)
