# Generated by Django 4.1.1 on 2022-09-07 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("referensi", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DetailPasien",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("HB", models.CharField(max_length=10)),
                ("LEUCO", models.CharField(max_length=10)),
                ("BT", models.CharField(max_length=10)),
                ("GDS", models.CharField(max_length=10)),
                ("ERY", models.CharField(max_length=10)),
                ("CT", models.CharField(max_length=10)),
                ("golongan_darah", models.CharField(max_length=10)),
                ("HBSAG", models.CharField(max_length=10)),
                ("HT", models.CharField(max_length=10)),
                ("THROMBO", models.CharField(max_length=10)),
                ("HIV", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Pasien",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nomor_seri", models.CharField(max_length=20)),
                ("nama", models.CharField(max_length=50)),
                ("nomor_ktp", models.CharField(max_length=16)),
                ("tempat_lahir", models.CharField(max_length=30)),
                ("tanggal_lahir", models.DateField(max_length=30)),
                ("umur", models.CharField(max_length=50)),
                ("jenis_kelamin", models.CharField(max_length=1)),
                ("alamat", models.CharField(max_length=100)),
                ("daerah", models.CharField(max_length=50)),
                ("pulau", models.CharField(max_length=50)),
                ("nomor_telepon", models.CharField(max_length=15)),
                ("nama_keluarga", models.CharField(max_length=50)),
                ("nomor_telepon_keluarga", models.CharField(max_length=15)),
                ("perlu_rescreen", models.BooleanField(default=False)),
                ("perlu_radiologi", models.BooleanField(default=False)),
                ("perlu_ekg", models.BooleanField(default=False)),
                ("diagnosa", models.CharField(max_length=50, null=True)),
                ("nomor_antrian", models.PositiveSmallIntegerField(null=True)),
                ("telah_daftar", models.BooleanField(default=False)),
                ("jam_daftar", models.DateTimeField(null=True)),
                ("status", models.CharField(max_length=30, null=True)),
                (
                    "penyakit",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="referensi.penyakit",
                    ),
                ),
                (
                    "puskemas",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="referensi.puskemas",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ScreeningPasien",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("telah_lewat_cek_tensi", models.BooleanField(null=True)),
                ("jam_cek_tensi", models.DateTimeField(null=True)),
                ("telah_lewat_pemeriksaan", models.BooleanField(null=True)),
                ("jam_pemeriksaan", models.DateTimeField(null=True)),
                ("telah_lewat_cek_lab", models.BooleanField(null=True)),
                ("jam_cek_lab", models.DateTimeField(null=True)),
                ("telah_lewat_cek_radiologi", models.BooleanField(null=True)),
                ("jam_cek_radiologi", models.DateTimeField(null=True)),
                ("telah_lewat_cek_ekg", models.BooleanField(null=True)),
                ("jam_cek_ekg", models.DateTimeField(null=True)),
                ("telah_lewat_cek_kartu_kuning", models.BooleanField(null=True)),
                ("jam_cek_kartu_kuning", models.DateTimeField(null=True)),
                ("nomor_kartu_kuning", models.CharField(max_length=20)),
                (
                    "pasien",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="pasien.pasien"
                    ),
                ),
            ],
        ),
    ]