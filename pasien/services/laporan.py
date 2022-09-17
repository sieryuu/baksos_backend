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

#yes this is horseshit but im going insane
def laporan_screening_excel():
    full_report = laporan_screening()

    workbook = Workbook()
    worksheet = workbook.active

    penyakit_list = list(full_report.keys())

    worksheet['A1'].value = 'Penyakit'
    for row, i in enumerate(penyakit_list):
        column_cell = 'A'
        worksheet[column_cell+str(row+2)] = str(i)

    header_list = list(full_report[penyakit_list[0]].keys())

    for col, entry in enumerate(header_list):
        worksheet.cell(row=1, column=col+2, value=entry)
    
    row = 2
    for penyakit in penyakit_list:
        penyakit_data = list(full_report[penyakit].values())
        for col, entry in enumerate(penyakit_data):
            worksheet.cell(row=row, column=col+2, value=entry)
        row += 1
    
    
    dim_holder = DimensionHolder(worksheet=worksheet)
    for col in range(worksheet.min_column, worksheet.max_column + 1):
        dim_holder[get_column_letter(col)] = ColumnDimension(
            worksheet, min=col, max=col, width=20
        )

    worksheet.column_dimensions = dim_holder

    tab = Table(displayName="Table1", ref=f"A1:M{worksheet.max_row}")
    style = TableStyleInfo(
        name="TableStyleLight8",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=True,
    )
    tab.tableStyleInfo = style
    worksheet.add_table(tab)
        
    return workbook
