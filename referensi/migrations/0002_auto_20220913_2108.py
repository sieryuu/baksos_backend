# Generated by Django 3.2.10 on 2022-09-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referensi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penyakit',
            name='waktu_dibuat',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='puskesmas',
            name='waktu_dibuat',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]