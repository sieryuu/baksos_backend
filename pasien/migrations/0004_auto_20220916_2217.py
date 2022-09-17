# Generated by Django 3.2.10 on 2022-09-16 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasien', '0003_auto_20220914_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='pasien',
            name='nama_pendamping',
            field=models.CharField(default='default', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pasien',
            name='nomor_telepon_pendamping',
            field=models.CharField(default='default', max_length=15),
            preserve_default=False,
        ),

        migrations.RunSQL("UPDATE pasien_pasien SET nama_pendamping = nama_keluarga;"),
        migrations.RunSQL("UPDATE pasien_pasien SET nomor_telepon_pendamping = nomor_telepon_keluarga;")

    ]
