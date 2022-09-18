from collections import defaultdict
from pasien.models import Pasien, ScreeningPasien, KartuKuning
from referensi.models import Puskesmas, Penyakit
from django.db.models import Q

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.worksheet.table import Table, TableStyleInfo


# this entire file has bad codes from the worst depths of hell
# pls forgive


def laporan_pendaftaran():
    pasien = Pasien.objects.all()
    pulaus = Puskesmas.objects.all().values_list("pulau", flat=True).distinct()
    penyakits = Penyakit.objects.all().values_list("nama", flat=True)

    full_report = []
    for pulau in pulaus:
        data = {}
        data["DAERAH"] = pulau
        for penyakit in penyakits:
            data[penyakit] = pasien.filter(
                penyakit=penyakit, puskesmas__pulau=pulau
            ).count()
        full_report.append(data)

    return full_report


def laporan_pendaftaran_excel():
    full_report = laporan_pendaftaran()

    colu = [row.pop("DAERAH") for row in full_report]

    workbook = Workbook()
    worksheet = workbook.active

    worksheet["A1"].value = "DAERAH"
    for row, i in enumerate(colu):
        column_cell = "A"
        worksheet[column_cell + str(row + 2)] = str(i)

    headers = full_report[0].keys()

    for col, entry in enumerate(headers):
        worksheet.cell(row=1, column=col + 2, value=entry)

    row = 2
    for data in full_report:
        for header in headers:
            for col, entry in enumerate(data):
                worksheet.cell(row=row, column=col + 2, value=data[header])
                col +=1
        row += 1

    return workbook


def laporan_kehadiran():
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
        rep["total_tidak_hadir"] = pasien.filter(
            diagnosa=penyakit, nomor_antrian__isnull=True
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
        rep["total_kehadiran_lab"] = screenings.filter(telah_lewat_cek_lab=True).count()
        rep["total_kehadiran_radiologi"] = screenings.filter(
            telah_lewat_cek_radiologi=True
        ).count()
        rep["total_kehadiran_ekg"] = screenings.filter(telah_lewat_cek_ekg=True).count()
        rep["total_kehadiran_hari_kedua"] = total_hari_kedua
        rep["total_kehadiran_rescreening"] = total_rescreen

    return full_report


def laporan_kehadiran_excel():
    full_report = laporan_kehadiran()

    workbook = Workbook()
    worksheet = workbook.active

    penyakit_list = list(full_report.keys())

    worksheet["A1"].value = "JenisPenyakit"
    for row, i in enumerate(penyakit_list):
        column_cell = "A"
        worksheet[column_cell + str(row + 2)] = str(i)

    header_list = list(full_report[penyakit_list[0]].keys())

    for col, entry in enumerate(header_list):
        worksheet.cell(row=1, column=col + 2, value=entry)

    row = 2
    for penyakit in penyakit_list:
        penyakit_data = list(full_report[penyakit].values())
        for col, entry in enumerate(penyakit_data):
            worksheet.cell(row=row, column=col + 2, value=entry)
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


def laporan_screening():
    pasien = Pasien.objects.all()
    screenings = ScreeningPasien.objects.all()
    kartu_kunings = KartuKuning.objects.all()
    penyakits = pasien.values_list("diagnosa", flat=True)

    full_report = defaultdict(lambda: defaultdict(dict))
    for penyakit in penyakits:
        rep = full_report[penyakit]

        tidak_lulus_tensi = screenings.filter(telah_lewat_cek_tensi=False).count()
        tidak_lulus_fisik = (
            screenings.filter(telah_lewat_pemeriksaan=False)
            .exclude(pasien__penyakit__grup="KATARAK")
            .count()
        )
        tidak_lulus_mata = screenings.filter(
            telah_lewat_pemeriksaan=False, pasien__penyakit__grup="KATARAK"
        ).count()
        tidak_lulus_kk = screenings.filter(telah_lewat_cek_kartu_kuning=False).count()

        rep["total_hadir"] = pasien.filter(
            diagnosa=penyakit, nomor_antrian__isnull=False
        ).count()
        rep["total_pasien_lolos_kk"] = kartu_kunings.filter(status="LOLOS").count()
        rep["total_pasien_lolos_kk_hari_pertama"] = kartu_kunings.filter(
            status="LOLOS", waktu_dibuat__date="2022-09-24"
        ).count()
        rep["total_pasien_lolos_kk_hari_kedua"] = kartu_kunings.filter(
            status="LOLOS", waktu_dibuat__date="2022-09-25"
        ).count()
        rep["total_tidak_lolos"] = (
            tidak_lulus_tensi + tidak_lulus_fisik + tidak_lulus_mata + tidak_lulus_kk
        )
        rep["tidak_lulus_tensi"] = tidak_lulus_tensi
        rep["tidak_lulus_fisik"] = tidak_lulus_fisik
        rep["tidak_lulus_mata"] = tidak_lulus_mata
        rep["tidak_lulus_kk"] = tidak_lulus_kk
        rep["total_pending_kk"] = kartu_kunings.filter(status="PENDING").count()
        rep["lolos_pending_hari_pertama"] = 0
        rep["lolos_pending_hari_kedua"] = 0

    return full_report


def laporan_screening_excel():
    full_report = laporan_screening()

    workbook = Workbook()
    worksheet = workbook.active

    penyakit_list = list(full_report.keys())

    worksheet["A1"].value = "JenisPenyakit"
    for row, i in enumerate(penyakit_list):
        column_cell = "A"
        worksheet[column_cell + str(row + 2)] = str(i)

    header_list = list(full_report[penyakit_list[0]].keys())

    for col, entry in enumerate(header_list):
        worksheet.cell(row=1, column=col + 2, value=entry)

    row = 2
    for penyakit in penyakit_list:
        penyakit_data = list(full_report[penyakit].values())
        for col, entry in enumerate(penyakit_data):
            worksheet.cell(row=row, column=col + 2, value=entry)
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
