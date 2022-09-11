from django_filters import rest_framework as filters
from .models import Pasien


class PasienFilterset(filters.FilterSet):
    class Meta:
        model = Pasien
        fields = {
            "nomor_seri",
            "puskesmas",
            "penyakit",
            "nama",
            "nomor_identitas",
            "tipe_identitas",
            "tempat_lahir",
            "tanggal_lahir",
            "umur",
            "jenis_kelamin",
            "alamat",
            "daerah",
            "pulau",
            "nomor_telepon",
            "nama_keluarga",
            "nomor_telepon_keluarga",
            "perlu_rescreen",
            "perlu_radiologi",
            "perlu_ekg",
            "diagnosa",
            "nomor_antrian",
            "tanggal_nomor_antrian",
            "last_status",
            "komentar",
            "penyakit__grup",
        }
