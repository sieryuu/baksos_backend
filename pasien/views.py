from django.db import transaction
from django.http import HttpResponse
from openpyxl.writer.excel import save_virtual_workbook
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from pasien.models import DetailPasien, Pasien, ScreeningPasien
from pasien.serializer import (CapKehadiranKartuKuningSerializer,
                               CapKehadiranLabSerializer,
                               CapKehadiranRadiologiSerializer,
                               CapKehadiranSerializer, DetailPasienSerializer,
                               ImportPasienSerializer, KartuKuningSerializer,
                               PasienSerializer, ScreeningPasienSerializer)
from pasien.services import pasien as PasienService
from pasien.services import screening_pasien as ScreeningPasienService
from django_filters import rest_framework as filters

# Create your views here.
class PasienViewSet(viewsets.ModelViewSet):
    queryset = Pasien.objects.all()
    serializer_class = PasienSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = '__all__'

    @action(detail=False, methods=["get"])
    def template(self, request, pk=None):
        workbook = PasienService.generate_import_template()
        response = HttpResponse(
            content=save_virtual_workbook(workbook),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=PasienTemplate.xlsx"
        return response

    @action(detail=False, methods=["post"])
    def import_pasien(self, request, pk=None):
        try:
            serializer = ImportPasienSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            PasienService.import_pasien(file=serializer.validated_data["file"])
            response = HttpResponse(
                content="Import File Sukses!",
            )
            return response
        except Exception as ex:
            raise ex

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def update_penyakit(self, request, pk=None):
        pasien: Pasien = self.get_object()
        penyakit = request.data["penyakit"]

        PasienService.update_penyakit(pasien=pasien, penyakit=penyakit)

        return Response(
            f"Penyakit pasien {pasien.nama} sudah diperbaharui menjadi {penyakit}!"
        )

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def update_diagnosa(self, request, pk=None):
        pasien: Pasien = self.get_object()

        diagnosa = request.data["diagnosa"]

        PasienService.update_diagnosa(pasien=pasien, diagnosa=diagnosa)

        return Response(
            f"Diagnosa pasien {pasien.nama} sudah diperbaharui menjadi {diagnosa}!"
        )


class DetailPasienViewSet(viewsets.ModelViewSet):
    queryset = DetailPasien.objects.all()
    serializer_class = DetailPasienSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = '__all__'

class ScreeningPasienViewSet(viewsets.ModelViewSet):
    queryset = ScreeningPasien.objects.all()
    serializer_class = ScreeningPasienSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = '__all__'

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_cek_tensi(self, request, pk=None):
        serializer = CapKehadiranSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        pasien_id = serializer.validated_data["pasien_id"]

        ScreeningPasienService.hadir_tensi(kehadiran=kehadiran, pasien_id=pasien_id)

        return Response("Berhasil mencatat kehadiran Tensi!")

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_pemeriksaan(self, request, pk=None):
        serializer = CapKehadiranSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        pasien_id = serializer.validated_data["pasien_id"]

        ScreeningPasienService.hadir_pemeriksaan(
            kehadiran=kehadiran, pasien_id=pasien_id
        )

        return Response("Berhasil mencatat kehadiran Pemeriksaan!")

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_lab(self, request, pk=None):
        serializer = CapKehadiranLabSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        perlu_ekg = serializer.validated_data["perlu_ekg"]
        perlu_radiologi = serializer.validated_data["perlu_radiologi"]
        pasien_id = serializer.validated_data["pasien_id"]

        ScreeningPasienService.hadir_lab(
            kehadiran=kehadiran,
            pasien_id=pasien_id,
            perlu_ekg=perlu_ekg,
            perlu_radiologi=perlu_radiologi,
        )

        return Response("Berhasil mencatat kehadiran Lab!")

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_radiologi(self, request, pk=None):
        serializer = CapKehadiranRadiologiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        tipe_hasil_rontgen = serializer.validated_data["tipe_hasil_rontgen"]
        nomor_kertas_penyerahan = serializer.validated_data.get(
            "nomor_kertas_penyerahan"
        )
        pasien_id = serializer.validated_data["pasien_id"]

        ScreeningPasienService.hadir_radiologi(
            kehadiran=kehadiran,
            pasien_id=pasien_id,
            tipe_hasil_rontgen=tipe_hasil_rontgen,
            nomor_kertas_penyerahan=nomor_kertas_penyerahan,
        )

        return Response("Berhasil mencatat kehadiran Radiologi!")

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_ekg(self, request, pk=None):
        serializer = CapKehadiranSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        pasien_id = serializer.validated_data["pasien_id"]

        ScreeningPasienService.hadir_ekg(kehadiran=kehadiran, pasien_id=pasien_id)

        return Response("Berhasil mencatat kehadiran EKG!")

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_kartu_kuning(self, request, pk=None):
        serializer = CapKehadiranKartuKuningSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        pasien_id = serializer.validated_data["pasien_id"]
        status = serializer.validated_data["status"]

        tanggal = serializer.validated_data.get("tanggal")
        jam = serializer.validated_data.get("jam")
        perhatian = serializer.validated_data.get("perhatian")

        kartu_kuning = ScreeningPasienService.hadir_kartu_kuning(
            kehadiran=kehadiran,
            pasien_id=pasien_id,
            status=status,
            tanggal=tanggal,
            jam=jam,
            perhatian=perhatian,
        )

        serializer = KartuKuningSerializer(kartu_kuning)

        return Response(serializer.data)
