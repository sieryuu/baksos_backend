from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter
from datetime import datetime
from pasien.models import Pasien
from referensi.models import Penyakit, Puskemas


def generate_import_template():
    workbook = Workbook()
    worksheet = workbook.active

    headers = [
        "Nomor Seri",
        "Puskesmas",
        "Penyakit",
        "Nama",
        "Nomor KTP",
        "Tempat Lahir",
        "Tanggal Lahir",
        "Jenis Kelamin",
        "Alamat",
        "Daerah",
        "Pulau",
        "Nomor Telepon",
        "Nama Keluarga",
        "Nomor Telepon Keluarga",
    ]

    worksheet.append(headers)

    dim_holder = DimensionHolder(worksheet=worksheet)

    for col in range(worksheet.min_column, worksheet.max_column + 1):
        dim_holder[get_column_letter(col)] = ColumnDimension(
            worksheet, min=col, max=col, width=20
        )

    worksheet.column_dimensions = dim_holder

    tab = Table(displayName="Table1", ref="A1:N2")
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

    if worksheet["A1"].value != "Nomor Seri":
        raise Exception("Invalid file, please check again!")

    puskemas_list = Puskemas.objects.all()
    penyakit_list = Penyakit.objects.all()

    now = datetime.now()

    new_patients = []
    for row in worksheet.iter_rows(
        min_row=2, min_col=1, max_row=worksheet.max_row, max_col=worksheet.max_column
    ):
        date_of_birth = now - row[6].value
        years = (date_of_birth.total_seconds()/ (365.242*24*3600))
        tahun=int(years)

        months=(years-tahun)*12
        bulan=int(months)

        umur = f'{tahun} tahun {bulan} bulan'

        new_patients.append(Pasien(
            nomor_seri=row[0].value,
            puskemas=puskemas_list.get(puskesmas=row[1].value),
            penyakit=penyakit_list.get(nama=row[2].value),
            nama=row[3].value,
            nomor_ktp=row[4].value,
            tempat_lahir=row[5].value,
            tanggal_lahir=row[6].value,
            umur=umur,
            jenis_kelamin=row[7].value,
            alamat=row[8].value,
            daerah=row[9].value,
            pulau=row[10].value,
            nomor_telepon=row[11].value,
            nama_keluarga=row[12].value,
            nomor_telepon_keluarga=row[13].value
        )
        )

    Pasien.objects.bulk_create(new_patients)
