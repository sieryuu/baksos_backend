# Generated by Django 3.2.10 on 2022-09-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Penyakit',
            fields=[
                ('waktu_dibuat', models.DateTimeField(auto_created=True)),
                ('dibuat_oleh', models.CharField(max_length=50)),
                ('diperbaharui_oleh', models.CharField(max_length=50)),
                ('waktu_diperbaharui', models.DateTimeField(auto_now=True)),
                ('nama', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('grup', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Puskesmas',
            fields=[
                ('waktu_dibuat', models.DateTimeField(auto_created=True)),
                ('dibuat_oleh', models.CharField(max_length=50)),
                ('diperbaharui_oleh', models.CharField(max_length=50)),
                ('waktu_diperbaharui', models.DateTimeField(auto_now=True)),
                ('puskesmas', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('pulau', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
