from collections import defaultdict
from pasien.models import Pasien, ScreeningPasien
from django.db.models import Q

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.worksheet.table import Table, TableStyleInfo


def laporan_screening():
    pasien = Pasien.objects.all()
    screenings = ScreeningPasien.objects.all()
    penyakits = pasien.values_list("diagnosa", flat=True)

    full_report = defaultdict(lambda: defaultdict(dict))
    for penyakit in penyakits:
        rep = full_report[penyakit]

        total_hari_pertama = pasien.filter(
            Q(tanggal_nomor_antrian__date="2022-09-24")
            | Q(tanggal_nomor_antrian_pertama__date="2022-09-24"),
            diagnosa=penyakit,
        ).count()
        total_hari_kedua = pasien.filter(
            diagnosa=penyakit, tanggal_nomor_antrian__date="2022-09-24"
        ).count()
        total_rescreen = pasien.filter(perlu_rescreen=True).count()

        rep["total_daftar"] = pasien.filter(diagnosa=penyakit).count()
        rep["total_hadir"] = pasien.filter(
            diagnosa=penyakit, nomor_antrian__isnull=False
        ).count()
        rep["total_pasien_hadir"] = (
            total_hari_pertama + total_hari_kedua - total_rescreen
        )
        rep["total_kehadiran_hari_pertama"] = total_hari_pertama
        rep["total_kehadiran_pendaftaran"] = pasien.filter(
            diagnosa=penyakit, tanggal_nomor_antrian__date="2022-09-24"
        ).count()
        rep["total_kehadiran_fisik"] = (
            screenings.filter(telah_lewat_pemeriksaan=True)
            .exclude(pasien__penyakit__grup="MATA")
            .count()
        )
        rep["total_kehadiran_mata"] = screenings.filter(
            telah_lewat_pemeriksaan=True, pasien__penyakit__grup="KATARAK"
        ).count()
        rep["total_kehadiran_lab"] = screenings.filter(
            telah_lewat_cek_lab=True
        ).count()
        rep["total_kehadiran_radiologi"] = screenings.filter(
            telah_lewat_cek_radiologi=True
        ).count()
        rep["total_kehadiran_ekg"] = screenings.filter(
            telah_lewat_cek_ekg=True
        ).count()
        rep["total_kehadiran_hari_kedua"] = total_hari_kedua
        rep["total_kehadiran_rescreening"] = total_rescreen
    
    return full_report

def laporan_screening_excel():
    full_report = laporan_screening()

    workbook = Workbook()
    ws = workbook.active

    penyakit_list = full_report.keys()

    for col in ws.iter_rows(min_row=1, max_col=1):
        for cell in col:
            print(cell)
        
    return workbook
