from typing import Iterable, Optional

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import UniqueConstraint
from common.models import CrudModel, CrudModelManager

from referensi.models import Penyakit, Puskesmas

class PasienManager(CrudModelManager):
    pass

# Create your models here.
class Pasien(CrudModel):
    nomor_seri = models.CharField(max_length=20, unique=True)
    puskesmas = models.ForeignKey(Puskesmas, on_delete=models.CASCADE)
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
    nomor_antrian = models.CharField(max_length=10, null=True)
    tanggal_nomor_antrian = models.DateTimeField(null=True)
    last_status = models.CharField(max_length=30, null=True)
    komentar = models.CharField(max_length=255, null=True)

    objects = PasienManager() 

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["nama", "tanggal_lahir"], name="unique_name_and_dob"
            )
        ]

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = "default",
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        if self.nomor_antrian and self.tanggal_nomor_antrian:
            if Pasien.objects.filter(
                nomor_antrian=self.nomor_antrian,
                penyakit__grup=self.penyakit.grup,
                tanggal_nomor_antrian__date=self.tanggal_nomor_antrian.date(),
            ):
                raise Exception(f"Nomor antrian {self.penyakit.nama}/{self.nomor_antrian} duplikat!")

        if self.pk is None:
            self.diagnosa = self.penyakit.pk

        return super().save(force_insert, force_update, using, update_fields)


class ScreeningPasien(CrudModel):
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


class DetailPasien(CrudModel):
    tensi = models.CharField(max_length=100)
    HB = models.CharField(max_length=100)
    LEUCO = models.CharField(max_length=100)
    BT = models.CharField(max_length=100)
    GDS = models.CharField(max_length=100)
    ERY = models.CharField(max_length=100)
    CT = models.CharField(max_length=100)
    golongan_darah = models.CharField(max_length=100)
    HBSAG = models.CharField(max_length=100)
    HT = models.CharField(max_length=100)
    THROMBO = models.CharField(max_length=100)
    HIV = models.CharField(max_length=100)


class KartuKuning(CrudModel):
    pasien = models.OneToOneField(Pasien, on_delete=models.CASCADE)
    nomor = models.CharField(max_length=10)
    tanggal_operasi = models.DateField(null=True)
    jam_operasi = models.TimeField(null=True)
    perhatian = ArrayField(models.CharField(max_length=50), null=True)
    status = models.CharField(max_length=10)
    komentar = models.CharField(max_length=255, null=True)
