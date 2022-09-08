from typing import Iterable, Optional
from django.db import models

from referensi.models import Penyakit, Puskesmas
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Pasien(models.Model):
    nomor_seri = models.CharField(max_length=20)
    puskemas = models.ForeignKey(Puskesmas, on_delete=models.CASCADE)
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    nomor_identitas = models.CharField(max_length=16, unique=True)
    tipe_identitas = models.CharField(max_length=29)
    tempat_lahir = models.CharField(max_length=30)
    tanggal_lahir = models.DateField(max_length=30)
    umur = models.CharField(max_length=50)
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
    nomor_antrian = models.PositiveSmallIntegerField(null=True)
    tanggal_nomor_antrian = models.DateTimeField(null=True)
    telah_daftar = models.BooleanField(default=False)
    jam_daftar = models.DateTimeField(null=True)
    status = models.CharField(max_length=30, null=True)

    class Meta:
       indexes = [
            models.Index(fields=['nama', 'tanggal_lahir']),
        ]

    def save(
        self,
        force_insert: bool = ...,
        force_update: bool = ...,
        using: Optional[str] = ...,
        update_fields: Optional[Iterable[str]] = ...,
    ) -> None:
        if Pasien.objects.filter(
            nomor_antrian=self.nomor_antrian,
            penyakit=self.penyakit,
            tanggal_nomor_antrian__date=self.tanggal_nomor_antrian.date,
        ):
            raise Exception("Nomor antrian duplikat!")

        if self.pk is None:
            self.diagnosa = self.penyakit.pk

        return super().save(force_insert, force_update, using, update_fields)


class ScreeningPasien(models.Model):
    pasien = models.OneToOneField(Pasien, on_delete=models.CASCADE)
    telah_lewat_cek_tensi = models.BooleanField(null=True)
    jam_cek_tensi = models.DateTimeField(null=True)
    telah_lewat_pemeriksaan = models.BooleanField(null=True)
    petugas_cek_tensi = models.CharField(max_length=50, null=True)
    jam_pemeriksaan = models.DateTimeField(null=True)
    petugas_pemeriksaaan = models.CharField(max_length=50, null=True)
    telah_lewat_cek_lab = models.BooleanField(null=True)
    jam_cek_lab = models.DateTimeField(null=True)
    petugas_cek_lab = models.CharField(max_length=50, null=True)
    telah_lewat_cek_radiologi = models.BooleanField(null=True)
    jam_cek_radiologi = models.DateTimeField(null=True)
    petugas_cek_radiologi = models.CharField(max_length=50, null=True)
    tipe_hasil_rontgen = models.CharField(max_length=5, null=True)
    nomor_kertas_penyerahan = models.CharField(max_length=50, null=True)
    telah_lewat_cek_ekg = models.BooleanField(null=True)
    jam_cek_ekg = models.DateTimeField(null=True)
    petugas_cek_ekg = models.CharField(max_length=50, null=True)
    telah_lewat_cek_kartu_kuning = models.BooleanField(null=True)
    jam_cek_kartu_kuning = models.DateTimeField(null=True)
    petugas_cek_kartu_kuning = models.CharField(max_length=50, null=True)
    nomor_kartu_kuning = models.CharField(max_length=20)


class DetailPasien(models.Model):
    tensi = models.CharField(max_length=10)
    HB = models.CharField(max_length=10)
    LEUCO = models.CharField(max_length=10)
    BT = models.CharField(max_length=10)
    GDS = models.CharField(max_length=10)
    ERY = models.CharField(max_length=10)
    CT = models.CharField(max_length=10)
    golongan_darah = models.CharField(max_length=10)
    HBSAG = models.CharField(max_length=10)
    HT = models.CharField(max_length=10)
    THROMBO = models.CharField(max_length=10)
    HIV = models.CharField(max_length=10)


class KartuKuning(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE)
    harap_datang_ke = models.CharField(max_length=100, null=True)
    tanggal_operasi = models.DateTimeField(null=True)
    jam_operasi = models.TimeField(null=True)
    perhatian = ArrayField(models.CharField(max_length=50), null=True)
    status = models.CharField(max_length=10)
    komentar = models.CharField(max_length=255, null=True)
