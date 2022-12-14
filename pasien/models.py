from typing import Iterable, Optional

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import UniqueConstraint
from common.models import CrudModel, CrudModelManager

from referensi.models import Penyakit, Puskesmas

from django.core.exceptions import ValidationError


class PasienManager(CrudModelManager):
    pass


# Create your models here.
class Pasien(CrudModel):
    nomor_seri = models.CharField(max_length=20, unique=True)
    puskesmas = models.ForeignKey(Puskesmas, on_delete=models.CASCADE)
    penyakit = models.ForeignKey(Penyakit, on_delete=models.CASCADE)
    nama = models.CharField(max_length=50)
    nomor_identitas = models.CharField(max_length=30, unique=True)
    tipe_identitas = models.CharField(max_length=29)
    tempat_lahir = models.CharField(max_length=30)
    tanggal_lahir = models.DateField(max_length=30)
    umur = models.CharField(max_length=50)
    jenis_kelamin = models.CharField(max_length=1)
    alamat = models.CharField(max_length=100)
    daerah = models.CharField(max_length=50)
    pulau = models.CharField(max_length=50)
    nomor_telepon = models.CharField(max_length=30)
    nama_keluarga = models.CharField(max_length=50)
    nomor_telepon_keluarga = models.CharField(max_length=30)
    nama_pendamping = models.CharField(max_length=50)
    nomor_telepon_pendamping = models.CharField(max_length=30)
    perlu_rescreen = models.BooleanField(default=False)
    perlu_radiologi = models.BooleanField(default=False)
    perlu_ekg = models.BooleanField(default=False)
    diagnosa = models.CharField(max_length=50, null=True)
    nomor_antrian = models.CharField(max_length=10, null=True)
    tanggal_nomor_antrian = models.DateTimeField(null=True)
    last_status = models.CharField(max_length=30, null=True)
    komentar = models.CharField(max_length=255, null=True)
    nomor_antrian_pertama = models.CharField(max_length=10, null=True)
    tanggal_nomor_antrian_pertama = models.DateTimeField(null=True)

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
        pulau = Puskesmas.objects.values_list("pulau", flat=True)

        if self.nomor_antrian and self.tanggal_nomor_antrian:
            if (
                Pasien.objects.filter(
                    nomor_antrian=self.nomor_antrian,
                    penyakit__grup=self.penyakit.grup,
                    tanggal_nomor_antrian__date=self.tanggal_nomor_antrian.date(),
                )
                .exclude(pk=self.pk)
                .exists()
            ):
                raise ValidationError(
                    f"Nomor antrian {self.penyakit.nama}/{self.nomor_antrian} duplikat!"
                )

        if self.pk is None:
            self.diagnosa = self.penyakit.pk
        else:
            if (
                self.diagnosa in ["MINOR GA", "MINOR LOKAL"]
                and self.penyakit_id == "BENJOLAN"
            ) or (self.diagnosa == "PTERYGIUM" and self.penyakit_id == "KATARAK"):
                pass
            else:
                self.diagnosa = self.penyakit.pk

        if self.daerah not in pulau:
            raise ValidationError(f"{self.daerah} tidak ada di daftar pulau!")

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
    pasien = models.OneToOneField(Pasien, on_delete=models.CASCADE)
    tensi = models.CharField(max_length=100, null=True, blank=True)
    HB = models.CharField(max_length=100, null=True, blank=True)
    LEUCO = models.CharField(max_length=100, null=True, blank=True)
    BT = models.CharField(max_length=100, null=True, blank=True)
    GDS = models.CharField(max_length=100, null=True, blank=True)
    ERY = models.CharField(max_length=100, null=True, blank=True)
    CT = models.CharField(max_length=100, null=True, blank=True)
    golongan_darah = models.CharField(max_length=100, null=True, blank=True)
    HBSAG = models.CharField(max_length=100, null=True, blank=True)
    HT = models.CharField(max_length=100, null=True, blank=True)
    THROMBO = models.CharField(max_length=100, null=True, blank=True)
    HIV = models.CharField(max_length=100, null=True, blank=True)


class KartuKuning(CrudModel):
    pasien = models.OneToOneField(Pasien, on_delete=models.CASCADE)
    nomor = models.CharField(max_length=10, unique=True)
    tanggal_operasi = models.DateField(null=True)
    jam_operasi = models.TimeField(null=True)
    perhatian = ArrayField(models.CharField(max_length=50), null=True)
    status = models.CharField(max_length=10)
    komentar = models.CharField(max_length=500, null=True)
