from rest_framework import serializers
from .models import DetailPasien, Pasien, ScreeningPasien
from django.core.validators import FileExtensionValidator


class PasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasien
        fields = '__all__'


class DetailPasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailPasien
        fields = '__all__'



class ScreeningPasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningPasien
        fields = '__all__'


class ImportPasienSerializer(serializers.Serializer):
    file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["xlsx"])]
    )

class CapKehadiranSerializer(serializers.Serializer):
    hadir = serializers.BooleanField()
    pasien = serializers.IntegerField()

class CapKehadiranLabSerializer(CapKehadiranSerializer):
    perlu_radiologi = serializers.BooleanField()
    perlu_ekg = serializers.BooleanField()


class CapKehadiranRadiologiSerializer(CapKehadiranSerializer):
    tipe_hasil_rontgen = serializers.CharField()
    nomor_kertas_penyerahan = serializers.CharField(required=False)
