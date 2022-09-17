from django.utils import timezone
from crum import get_current_user

from pasien.models import Pasien, ScreeningPasien

from django.db import transaction


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

    if kehadiran:
        screening_pasien.telah_lewat_cek_tensi = kehadiran
        screening_pasien.jam_cek_tensi = timezone.now()
        screening_pasien.petugas_cek_tensi = get_current_user().username
    screening_pasien.telah_lewat_pemeriksaan = kehadiran
    screening_pasien.jam_pemeriksaan = timezone.now()
    screening_pasien.petugas_pemeriksaaan = get_current_user().username
    pasien.last_status = "PEMERIKSAAN"

    screening_pasien.save()
    pasien.save()


def hadir_lab(
    kehadiran: bool,
    pasien_id: int,
    perlu_ekg: bool,
    perlu_radiologi: bool,
    diagnosa: str,
):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)

    screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
    screening_pasien.telah_lewat_cek_lab = kehadiran
    screening_pasien.jam_cek_lab = timezone.now()
    screening_pasien.petugas_cek_lab = get_current_user().username
    screening_pasien.save()

    pasien.last_status = "LAB"
    pasien.perlu_ekg = perlu_ekg
    pasien.perlu_radiologi = perlu_radiologi
    pasien.diagnosa = diagnosa
    pasien.save()


def hadir_radiologi(kehadiran: bool, pasien_id: int):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)

    screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
    screening_pasien.telah_lewat_cek_radiologi = kehadiran
    screening_pasien.jam_cek_radiologi = timezone.now()
    screening_pasien.save()

    pasien.last_status = "RADIOLOGI"
    pasien.save()


def hasil_radiologi(
    screening: ScreeningPasien,
    tipe_hasil_rontgen: str,
    nomor_kertas_penyerahan: str,
):
    screening.tipe_hasil_rontgen = tipe_hasil_rontgen
    screening.nomor_kertas_penyerahan = nomor_kertas_penyerahan
    screening.petugas_cek_radiologi = get_current_user().username
    screening.save()


def hadir_ekg(kehadiran: bool, pasien_id: int):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)
    screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
    screening_pasien.telah_lewat_cek_ekg = kehadiran
    screening_pasien.jam_cek_ekg = timezone.now()
    screening_pasien.petugas_cek_ekg = get_current_user().username
    screening_pasien.save()

    pasien.last_status = "EKG"
    pasien.save()


def hadir_kartu_kuning(kehadiran: bool, pasien_id: int):
    pasien: Pasien = Pasien.objects.get(id=pasien_id)
    screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
    screening_pasien.telah_lewat_cek_kartu_kuning = kehadiran
    screening_pasien.jam_cek_kartu_kuning = timezone.now()
    screening_pasien.petugas_cek_kartu_kuning = get_current_user().username
    screening_pasien.save()

    pasien.last_status = "KARTU KUNING"
    pasien.save()


def batal_tensi(screening: ScreeningPasien):
    screening.telah_lewat_cek_tensi = None
    screening.jam_cek_tensi = None
    screening.petugas_cek_tensi = None
    screening.save()


def batal_pemeriksaan(screening: ScreeningPasien):
    screening.telah_lewat_pemeriksaan = None
    screening.jam_pemeriksaan = None
    screening.petugas_pemeriksaaan = None

    # batalin tensi jg
    screening.telah_lewat_cek_tensi = None
    screening.jam_cek_tensi = None
    screening.petugas_cek_tensi = None
    screening.save()


def batal_lab(screening: ScreeningPasien):
    screening.telah_lewat_cek_lab = None
    screening.jam_cek_lab = None
    screening.petugas_cek_lab = None
    screening.save()

    pasien: Pasien = screening.pasien
    pasien.perlu_ekg = False
    pasien.perlu_radiologi = False
    pasien.save()


def batal_radiologi(screening: ScreeningPasien):
    screening.telah_lewat_cek_radiologi = None
    screening.jam_cek_radiologi = None
    screening.petugas_cek_radiologi = None
    screening.tipe_hasil_rontgen = None
    screening.nomor_kertas_penyerahan = None
    screening.save()


def batal_ekg(screening: ScreeningPasien):
    screening.telah_lewat_cek_ekg = None
    screening.jam_cek_ekg = None
    screening.petugas_cek_ekg = None
    screening.save()


def batal_kartu_kuning(screening: ScreeningPasien):
    screening.telah_lewat_cek_kartu_kuning = None
    screening.jam_cek_kartu_kuning = None
    screening.petugas_cek_kartu_kuning = None
    screening.save()
