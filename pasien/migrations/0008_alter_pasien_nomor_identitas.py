# Generated by Django 3.2.10 on 2022-09-20 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasien', '0007_auto_20220920_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasien',
            name='nomor_identitas',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
