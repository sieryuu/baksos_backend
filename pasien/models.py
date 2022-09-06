from django.db import models

from referensi.models import Penyakit, Puskemas

# Create your models here.
class Pasien(models.Model):
    nomor_seri = models.CharField(max_length=20)
    puskemas = models.ForeignKey(Puskemas, on_delete=models.CASCADE)
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    nomor_ktp = models.CharField(max_length=16)
    tempat_lahir = models.CharField(max_length=30)
    tanggal_lahir = models.DateField(max_length=30)
    umur = models.IntegerField() #not sure yet
    jenis_kelamin = models.CharField(max_length=1)
    alamat = models.CharField(max_length=100)
    daerah = models.CharField(max_length=50)
    pulau = models.CharField(max_length=50)
    nomor_telepon = models.CharField(max_length=15)
    nama_keluarga = models.CharField(max_length=50)
    nomor_telepon_keluarga = models.CharField(max_length=15)
    perlu_rescreen = models.BooleanField(default=False)
    perlu_radiologi = models.BooleanField(default=False)
    perlu_ekg = models.BooleanField(default=False)
    diagnosa = models.CharField(max_length=50, null=True)
    nomor_antrian = models.PositiveSmallIntegerField()
    telah_daftar = models.BooleanField(default=False)
    jam_daftar = models.DateTimeField(null=True)


class ScreeningPasien(models.Model):
    pasien = models.OneToOneField(Pasien, on_delete=models.CASCADE)
    telah_lewat_cek_tensi = models.BooleanField(null=True)
    jam_cek_tensi = models.DateTimeField(null=True)
    telah_lewat_cek_fisik = models.BooleanField(null=True)
    jam_cek_fisik = models.DateTimeField(null=True)    
    telah_lewat_cek_mata = models.BooleanField(null=True)
    jam_cek_mata = models.DateTimeField(null=True)    
    telah_lewat_cek_lab = models.BooleanField(null=True)
    jam_cek_lab = models.DateTimeField(null=True)    
    telah_lewat_cek_radiologi = models.BooleanField(null=True)
    jam_cek_radiologi = models.DateTimeField(null=True)    
    telah_lewat_cek_ekg = models.BooleanField(null=True)
    jam_cek_ekg = models.DateTimeField(null=True)
    telah_lewat_cek_kartu_kuning = models.BooleanField(null=True)
    jam_cek_kartu_kuning = models.DateTimeField(null=True)
    nomor_kartu_kuning = models.CharField(max_length=20)




