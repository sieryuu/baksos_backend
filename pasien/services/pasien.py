from datetime import datetime

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.worksheet.table import Table, TableStyleInfo

from pasien.models import Pasien
from referensi.models import Penyakit, Puskesmas


def generate_import_template():
    workbook = Workbook()
    worksheet = workbook.active

    worksheet['A1'] = 'Template Import Pasien'
    worksheet['A1'].font = Font(size=20)

    headers = [
        "Nomor Seri",
        "Puskesmas",
        "Penyakit",
        "Nama",
        "Nomor Identitas",
        "Tipe Identitas",
        "Tempat Lahir",
        "Tanggal Lahir",
        "Jenis Kelamin",
        "Alamat",
        "Daerah",
        "Nomor Telepon",
        "Nama Keluarga",
        "Nomor Telepon Keluarga",
    ]

    worksheet.move_range("A2:N2", rows=1, cols=1)
    worksheet.append(headers) 

    dim_holder = DimensionHolder(worksheet=worksheet)

    for col in range(worksheet.min_column, worksheet.max_column + 1):
        dim_holder[get_column_letter(col)] = ColumnDimension(
            worksheet, min=col, max=col, width=20
        )

    worksheet.column_dimensions = dim_holder

    tab = Table(displayName="Table1", ref="A3:N4")
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


def import_pasien(file):
    worksheet = load_workbook(file)

    worksheet = worksheet.active

    if worksheet["A1"].value != "Template Import Pasien":
        raise Exception("Invalid file, please check again!")

    puskesmas_list = Puskesmas.objects.all()
    penyakit_list = Penyakit.objects.all()

    now = datetime.now()

    new_patients = []
    for row in worksheet.iter_rows(
        min_row=4, min_col=1, max_row=worksheet.max_row, max_col=worksheet.max_column
    ):
        date_of_birth = now - row[7].value
        years = date_of_birth.total_seconds() / (365.242 * 24 * 3600)
        tahun = int(years)

        months = (years - tahun) * 12
        bulan = int(months)

        umur = f"{tahun} tahun {bulan} bulan"

        puskesmas = puskesmas_list.get(puskesmas=row[1].value)
        penyakit = penyakit_list.get(nama=row[2].value)

        new_patients.append(
            Pasien(
                nomor_seri=row[0].value,
                puskesmas=puskesmas,
                penyakit=penyakit,
                nama=row[3].value,
                nomor_identitas=row[4].value,
                tipe_identitas=row[5].value,
                tempat_lahir=row[6].value,
                tanggal_lahir=row[7].value,
                umur=umur,
                jenis_kelamin=row[8].value,
                alamat=row[9].value,
                daerah=row[10].value,
                pulau=puskesmas.pulau,
                nomor_telepon=row[11].value,
                nama_keluarga=row[12].value,
                nomor_telepon_keluarga=row[13].value,
                diagnosa = penyakit.pk
            )
        )

    Pasien.objects.bulk_create(new_patients)


def update_penyakit(pasien: Pasien, penyakit: str):
    pasien.penyakit_id = penyakit
    pasien.diagnosa = penyakit
    pasien.save()

def update_diagnosa(pasien: Pasien, diagnosa: str):
    pasien.diagnosa = diagnosa
    pasien.save()