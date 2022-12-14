from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from common.serializer import DEFAULT_READ_ONLY_FIELDS

from .models import DetailPasien, KartuKuning, Pasien, ScreeningPasien


class KartuKuningSerializer(serializers.ModelSerializer):
    class Meta:
        model = KartuKuning
        fields = "__all__"
        read_only_fields = DEFAULT_READ_ONLY_FIELDS


class PasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasien
        fields = "__all__"
        read_only_fields = DEFAULT_READ_ONLY_FIELDS

    def to_representation(self, instance):
        response = super().to_representation(instance)
        kartukuning = KartuKuningSerializer(getattr(instance, "kartukuning", None))
        response["kartukuning"] = kartukuning.data
        return response


class DetailPasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailPasien
        fields = "__all__"
        read_only_fields = DEFAULT_READ_ONLY_FIELDS


class ScreeningPasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningPasien
        fields = "__all__"
        read_only_fields = DEFAULT_READ_ONLY_FIELDS


class ImportPasienSerializer(serializers.Serializer):
    file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["xlsx"])]
    )


class CapKehadiranSerializer(serializers.Serializer):
    hadir = serializers.BooleanField()
    pasien_id = serializers.IntegerField()


class CapKehadiranLabSerializer(CapKehadiranSerializer):
    perlu_radiologi = serializers.BooleanField()
    perlu_ekg = serializers.BooleanField()
    diagnosa = serializers.CharField()


class HasilRadiologiSerializer(serializers.Serializer):
    tipe_hasil_rontgen = serializers.CharField()
    nomor_kertas_penyerahan = serializers.CharField(required=False, allow_blank=True)


class SerahKartuKuningSerializer(serializers.Serializer):
    status = serializers.CharField()
    tanggal = serializers.DateField(required=False, allow_null=True)
    jam = serializers.TimeField(required=False, allow_null=True)
    perhatian = serializers.ListField(required=False)
