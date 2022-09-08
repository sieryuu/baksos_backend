from datetime import datetime
from rest_framework import viewsets
from pasien.models import DetailPasien, Pasien, ScreeningPasien
from pasien.serializer import (
    CapKehadiranLabSerializer,
    CapKehadiranSerializer,
    DetailPasienSerializer,
    ImportPasienSerializer,
    PasienSerializer,
    ScreeningPasienSerializer,
)
from rest_framework.decorators import action
from pasien.services import pasien as PasienService
from django.http import HttpResponse
from openpyxl.writer.excel import save_virtual_workbook
from rest_framework.response import Response
from crum import get_current_user

# Create your views here.
class PasienViewSet(viewsets.ModelViewSet):
    queryset = Pasien.objects.all()
    serializer_class = PasienSerializer

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

    @action(detail=False, methods=["post"])
    def update_penyakit(self, request, pk=None):
        pasien: Pasien = self.get_object()

        pasien.penyakit_id = request.data['penyakit']
        pasien.diagnosa = request.data['penyakit']
        pasien.save()

        return Response('OK')
    
    @action(detail=False, methods=["post"])
    def update_diagnosa(self, request, pk=None):
        pasien: Pasien = self.get_object()

        pasien.penyakit_id = request.data['penyakit']
        pasien.diagnosa = request.data['diagnosa']
        pasien.save()

        return Response('OK')


class DetailPasienViewSet(viewsets.ModelViewSet):
    queryset = DetailPasien.objects.all()
    serializer_class = DetailPasienSerializer


class ScreeningPasienViewSet(viewsets.ModelViewSet):
    queryset = ScreeningPasien.objects.all()
    serializer_class = ScreeningPasienSerializer

    @action(detail=False, methods=["post"])
    def hadir_cek_tensi(self, request, pk=None):
        serializer = CapKehadiranSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        pasien = Pasien.objects.get(id=serializer.validated_data["pasien"])

        screening_pasien: ScreeningPasien = ScreeningPasien.objects.get_or_create(
            pasien=pasien
        )
        screening_pasien.telah_lewat_cek_tensi = kehadiran
        screening_pasien.jam_cek_tensi = datetime.now()
        screening_pasien.petugas_cek_tensi = get_current_user()
        screening_pasien.save()

        return Response("OK!")

    @action(detail=False, methods=["post"])
    def hadir_pemeriksaan(self, request, pk=None):
        serializer = CapKehadiranSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        pasien = Pasien.objects.get(id=serializer.validated_data["pasien"])

        screening_pasien: ScreeningPasien = ScreeningPasien.objects.get_or_create(
            pasien=pasien
        )
        screening_pasien.telah_lewat_pemeriksaan = kehadiran
        screening_pasien.jam_pemeriksaan = datetime.now()
        screening_pasien.petugas_pemeriksaaan = get_current_user()
        screening_pasien.save()

        return Response("OK!")

    @action(detail=False, methods=["post"])
    def hadir_lab(self, request, pk=None):
        serializer = CapKehadiranLabSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        perlu_ekg = serializer.validated_data["perlu_ekg"]
        perlu_radiologi = serializer.validated_data["perlu_radiologi"]

        pasien: Pasien = Pasien.objects.get(id=serializer.validated_data["pasien"])

        screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
        screening_pasien.telah_lewat_cek_lab = kehadiran
        screening_pasien.jam_cek_lab = datetime.now()
        screening_pasien.petugas_cek_lab = get_current_user()
        screening_pasien.save()

        pasien.perlu_ekg = perlu_ekg
        pasien.perlu_radiologi = perlu_radiologi
        pasien.save()

        return Response("OK!")

    @action(detail=False, methods=["post"])
    def hadir_radiologi(self, request, pk=None):
        serializer = CapKehadiranLabSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        tipe_hasil_rontgen = serializer.validated_data["tipe_hasil_rontgen"]
        nomor_kertas_penyerahan = serializer.validated_data.get(
            "nomor_kertas_penyerahan"
        )

        pasien = Pasien.objects.get(id=serializer.validated_data["pasien"])

        screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
        screening_pasien.telah_lewat_cek_radiologi = kehadiran
        screening_pasien.jam_cek_radiologi = datetime.now()
        screening_pasien.tipe_hasil_rontgen = tipe_hasil_rontgen
        if tipe_hasil_rontgen == "USB" and nomor_kertas_penyerahan is None:
            raise Exception("Nomor kertas penyerahan kosong!")
        screening_pasien.nomor_kertas_penyerahan = nomor_kertas_penyerahan
        screening_pasien.petugas_cek_radiologi = get_current_user()
        screening_pasien.save()

        return Response("OK!")

    @action(detail=False, methods=["post"])
    def hadir_ekg(self, request, pk=None):
        serializer = CapKehadiranSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kehadiran = serializer.validated_data["hadir"]
        pasien = Pasien.objects.get(id=serializer.validated_data["pasien"])

        screening_pasien: ScreeningPasien = ScreeningPasien.objects.get(pasien=pasien)
        screening_pasien.telah_lewat_cek_ekg = kehadiran
        screening_pasien.jam_cek_ekg = datetime.now()
        screening_pasien.petugas_cek_ekg = get_current_user()
        screening_pasien.save()

        return Response("OK!")
