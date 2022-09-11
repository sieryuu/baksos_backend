from cmath import tan
from datetime import date, datetime
from time import time
from django.utils import timezone
from crum import get_current_user

from pasien.models import KartuKuning, Pasien, ScreeningPasien

from django.core.exceptions import ValidationError

def hadir_tensi(kehadiran: bool, pasien_id: int):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)

    screening_pasien, created = ScreeningPasien.objects.get_or_create(pasien=pasien)
    screening_pasien.telah_lewat_cek_tensi = kehadiran
    screening_pasien.jam_cek_tensi = timezone.now()
    screening_pasien.petugas_cek_tensi = get_current_user().username
    pasien.last_status = "TENSI"

    screening_pasien.save()
    pasien.save()


def hadir_pemeriksaan(kehadiran: bool, pasien_id: int):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)

    screening_pasien, created = ScreeningPasien.objects.get_or_create(pasien=pasien)

    screening_pasien.telah_lewat_pemeriksaan = kehadiran
    screening_pasien.jam_pemeriksaan = timezone.now()
    screening_pasien.petugas_pemeriksaaan = get_current_user().username
    pasien.last_status = "PEMERIKSAAN"

    screening_pasien.save()
    pasien.save()


def hadir_lab(kehadiran: bool, pasien_id: int, perlu_ekg: bool, perlu_radiologi: bool):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)

    screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
    screening_pasien.telah_lewat_cek_lab = kehadiran
    screening_pasien.jam_cek_lab = timezone.now()
    screening_pasien.petugas_cek_lab = get_current_user().username
    screening_pasien.save()

    pasien.last_status = "LAB"
    pasien.perlu_ekg = perlu_ekg
    pasien.perlu_radiologi = perlu_radiologi
    pasien.save()


def hadir_radiologi(
    kehadiran: bool,
    pasien_id: int,
    tipe_hasil_rontgen: str,
    nomor_kertas_penyerahan: str,
):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)

    screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
    screening_pasien.telah_lewat_cek_radiologi = kehadiran
    screening_pasien.jam_cek_radiologi = timezone.now()
    screening_pasien.tipe_hasil_rontgen = tipe_hasil_rontgen

    if tipe_hasil_rontgen == "USB" and nomor_kertas_penyerahan is None:
        raise ValidationError("Nomor kertas penyerahan kosong!")

    screening_pasien.nomor_kertas_penyerahan = nomor_kertas_penyerahan
    screening_pasien.petugas_cek_radiologi = get_current_user().username
    screening_pasien.save()

    pasien.last_status = "RADIOLOGI"
    pasien.save()


def hadir_ekg(kehadiran: bool, pasien_id: int):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)
    screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
    screening_pasien.telah_lewat_cek_ekg = kehadiran
    screening_pasien.jam_cek_ekg = timezone.now()
    screening_pasien.petugas_cek_ekg = get_current_user().username
    screening_pasien.save()

    pasien.last_status = "EKG"
    pasien.save()


def hadir_kartu_kuning(
    kehadiran: bool,
    pasien_id: int,
    status: str,
    tanggal: date,
    jam: time,
    perhatian: list,
):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)
    screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
    screening_pasien.telah_lewat_cek_kartu_kuning = kehadiran
    screening_pasien.jam_cek_kartu_kuning = timezone.now()
    screening_pasien.petugas_cek_kartu_kuning = get_current_user().username
    screening_pasien.save()

    pasien.last_status = "KARTU KUNING"
    pasien.save()

    kartu_kuning: KartuKuning = KartuKuning()
    kartu_kuning.nomor = __generate_nomor_kartu_kuning()
    kartu_kuning.pasien = pasien
    kartu_kuning.jam_operasi = jam
    kartu_kuning.tanggal_operasi = tanggal
    kartu_kuning.perhatian = perhatian
    kartu_kuning.status = status
    kartu_kuning.save()

    return kartu_kuning


def __generate_nomor_kartu_kuning():
    prefix = "KK"
    running_no = 1
    last_record = KartuKuning.objects.all().order_by("-nomor").first()

    if last_record:
        last_running_no = int(last_record.nomor[-4:])
        running_no = running_no + last_running_no

    return prefix + str(running_no).zfill(4)
