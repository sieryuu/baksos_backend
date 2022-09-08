from django.db import models

# Create your models here.
class Puskemas(models.Model):
    puskesmas = models.CharField(max_length=30)
    pulau = models.CharField(max_length=30)

class Penyakit(models.Model):
    nama = models.CharField(max_length=10, primary_key=True)
