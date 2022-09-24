from django.db import transaction
from django.db.utils import IntegrityError
from django.http import HttpResponse
from openpyxl.writer.excel import save_virtual_workbook
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from pasien.filters import PasienFilterset
from pasien.models import DetailPasien, Pasien, ScreeningPasien, KartuKuning
from pasien.serializer import (
    SerahKartuKuningSerializer,
    CapKehadiranLabSerializer,
    CapKehadiranSerializer,
    DetailPasienSerializer,
    HasilRadiologiSerializer,
    ImportPasienSerializer,
    PasienSerializer,
    ScreeningPasienSerializer,
    KartuKuningSerializer,
)
from pasien.services import pasien as PasienService
from pasien.services import screening_pasien as ScreeningPasienService
from pasien.services import laporan as LaporanService
from django_filters import rest_framework as filters
from rest_framework import status, filters as rest_filters
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from common.models import check_user_permission

# Create your views here.
class PasienViewSet(viewsets.ModelViewSet):
    queryset = Pasien.objects.all().order_by("nomor_seri").select_related("kartukuning")
    serializer_class = PasienSerializer
    filter_backends = (filters.DjangoFilterBackend, rest_filters.SearchFilter)
    filterset_fields = "__all__"
    filterset_class = PasienFilterset
    search_fields = ["nama", "nomor_identitas", "nomor_telepon"]

    def create(self, request, *args, **kwargs):
        try:
            resp = super().create(request, *args, **kwargs)
        except IntegrityError as err:
            if str(err).startswith(
                'duplicate key value violates unique constraint "unique_name_and_dob"'
            ):
                aa = str(err)[
                    len(
                        'duplicate key value violates unique constraint "unique_name_and_dob"\nDETAIL:  Key (nama, tanggal_lahir)=('
                    ) :
                ]
                bb = aa[0 : aa.index(") already exists")]
                split_str = bb.split(", ")
                return Response(
                    f"Data Nama ({split_str[0]}) dan Tanggal Lahir ({split_str[1]}) yang ditaruh telah terdaftar.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return resp

    def update(self, request, *args, **kwargs):
        try:
            resp = super().update(request, *args, **kwargs)
        except IntegrityError as err:
            if str(err).startswith(
                'duplicate key value violates unique constraint "unique_name_and_dob"'
            ):
                aa = str(err)[
                    len(
                        'duplicate key value violates unique constraint "unique_name_and_dob"\nDETAIL:  Key (nama, tanggal_lahir)=('
                    ) :
                ]
                bb = aa[0 : aa.index(") already exists")]
                split_str = bb.split(", ")
                return Response(
                    f"Data Nama ({split_str[0]}) dan Tanggal Lahir ({split_str[1]}) yang ditaruh telah terdaftar.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return resp

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
        except IntegrityError as err:
            if str(err).startswith(
                'duplicate key value violates unique constraint "unique_name_and_dob"'
            ):
                aa = str(err)[
                    len(
                        'duplicate key value violates unique constraint "unique_name_and_dob"\nDETAIL:  Key (nama, tanggal_lahir)=('
                    ) :
                ]
                bb = aa[0 : aa.index(") already exists")]
                split_str = bb.split(", ")
                return Response(
                    f"Data Nama ({split_str[0]}) dan Tanggal Lahir ({split_str[1]}) yang ditaruh telah terdaftar.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @check_user_permission(['lab'])
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

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def serah_nomor_antrian(self, request, pk=None):
        try:
            pasien = self.get_object()

            nomor_antrian = request.data.get("nomor_antrian")

            if nomor_antrian is None:
                raise ValidationError("Nomor antrian kosong!")

            PasienService.serah_nomor_antrian(
                pasien=pasien, nomor_antrian=nomor_antrian
            )

            return Response(
                f"Pasien {pasien.nama} sudah diserahkan nomor antrian {nomor_antrian}!"
            )
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def batal_nomor_antrian(self, request, pk=None):
        try:
            pasien = self.get_object()

            PasienService.batal_nomor_antrian(pasien=pasien)

            return Response(f"Antrian pasien {pasien.nama} sudah dibatalkan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def serah_kartu_kuning(self, request, pk=None):
        try:
            serializer = SerahKartuKuningSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            pasien = self.get_object()

            status_kk = serializer.validated_data["status"]
            tanggal = serializer.validated_data.get("tanggal")
            jam = serializer.validated_data.get("jam")
            perhatian = serializer.validated_data.get("perhatian")

            PasienService.serah_kartu_kuning(
                pasien=pasien,
                status=status_kk,
                tanggal=tanggal,
                jam=jam,
                perhatian=perhatian,
            )

            return Response(f"Pasien {pasien.nama} sudah diserahkan kartu kuning!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def batal_serah_kartu_kuning(self, request, pk=None):
        try:
            pasien = self.get_object()

            PasienService.batal_serah_kartu_kuning(pasien=pasien)

            return Response(f"Kartu Kuning pasien {pasien.nama} sudah dibatalkan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def pending_tensi(self, request, pk=None):
        try:
            pasien = self.get_object()

            PasienService.pending_tensi(pasien=pasien)

            return Response(f"Pasien {pasien.nama} telah pending tensi!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetailPasienViewSet(viewsets.ModelViewSet):
    queryset = DetailPasien.objects.all()
    serializer_class = DetailPasienSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = "__all__"


class ScreeningPasienViewSet(viewsets.ModelViewSet):
    queryset = ScreeningPasien.objects.all()
    serializer_class = ScreeningPasienSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = "__all__"

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_cek_tensi(self, request, pk=None):
        try:
            serializer = CapKehadiranSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            kehadiran = serializer.validated_data["hadir"]
            pasien_id = serializer.validated_data["pasien_id"]

            ScreeningPasienService.hadir_tensi(kehadiran=kehadiran, pasien_id=pasien_id)

            return Response("Berhasil mencatat kehadiran Tensi!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @check_user_permission(allowed_users=['pemeriksaan_mata', 'pemeriksaan_fisik'])
    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_pemeriksaan(self, request, pk=None):
        try:
            serializer = CapKehadiranSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            kehadiran = serializer.validated_data["hadir"]
            pasien_id = serializer.validated_data["pasien_id"]

            ScreeningPasienService.hadir_pemeriksaan(
                kehadiran=kehadiran, pasien_id=pasien_id
            )

            return Response("Berhasil mencatat kehadiran Pemeriksaan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_lab(self, request, pk=None):
        try:
            serializer = CapKehadiranLabSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            kehadiran = serializer.validated_data["hadir"]
            perlu_ekg = serializer.validated_data["perlu_ekg"]
            perlu_radiologi = serializer.validated_data["perlu_radiologi"]
            diagnosa = serializer.validated_data["diagnosa"]
            pasien_id = serializer.validated_data["pasien_id"]

            ScreeningPasienService.hadir_lab(
                kehadiran=kehadiran,
                pasien_id=pasien_id,
                perlu_ekg=perlu_ekg,
                perlu_radiologi=perlu_radiologi,
                diagnosa=diagnosa,
            )

            return Response("Berhasil mencatat kehadiran Lab!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_radiologi(self, request, pk=None):
        try:
            serializer = CapKehadiranSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            kehadiran = serializer.validated_data["hadir"]
            pasien_id = serializer.validated_data["pasien_id"]

            ScreeningPasienService.hadir_radiologi(
                kehadiran=kehadiran, pasien_id=pasien_id
            )

            return Response("Berhasil mencatat kehadiran Radiologi!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(detail=True, methods=["post"])
    def hasil_radiologi(self, request, pk=None):
        try:
            screening = self.get_object()

            serializer = HasilRadiologiSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            tipe_hasil_rontgen = serializer.validated_data["tipe_hasil_rontgen"]
            nomor_kertas_penyerahan = serializer.validated_data.get(
                "nomor_kertas_penyerahan"
            )

            ScreeningPasienService.hasil_radiologi(
                screening=screening,
                tipe_hasil_rontgen=tipe_hasil_rontgen,
                nomor_kertas_penyerahan=nomor_kertas_penyerahan,
            )

            return Response("Berhasil mencatat hasil Radiologi!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_ekg(self, request, pk=None):
        try:
            serializer = CapKehadiranSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            kehadiran = serializer.validated_data["hadir"]
            pasien_id = serializer.validated_data["pasien_id"]

            ScreeningPasienService.hadir_ekg(kehadiran=kehadiran, pasien_id=pasien_id)

            return Response("Berhasil mencatat kehadiran EKG!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def hadir_kartu_kuning(self, request, pk=None):
        try:
            serializer = CapKehadiranSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            kehadiran = serializer.validated_data["hadir"]
            pasien_id = serializer.validated_data["pasien_id"]

            ScreeningPasienService.hadir_kartu_kuning(
                kehadiran=kehadiran, pasien_id=pasien_id
            )

            return Response("Berhasil mencatat kehadiran KartU Kuning!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_classes((IsAdminUser,))
    @transaction.atomic
    @action(detail=True, methods=["post"])
    def batal_tensi(self, request, pk=None):
        try:
            screening = self.get_object()

            ScreeningPasienService.batal_pemeriksaan(screening)

            return Response("Tensi berhasil dibatalkan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_classes((IsAdminUser,))
    @transaction.atomic
    @action(detail=True, methods=["post"])
    def batal_tensi(self, request, pk=None):
        try:
            screening = self.get_object()

            ScreeningPasienService.batal_tensi(screening)

            return Response("Tensi berhasil dibatalkan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_classes((IsAdminUser,))
    @transaction.atomic
    @action(detail=True, methods=["post"])
    def batal_pemeriksaan(self, request, pk=None):
        try:
            screening = self.get_object()

            ScreeningPasienService.batal_pemeriksaan(screening)

            return Response("Pemeriksaan berhasil dibatalkan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_classes((IsAdminUser,))
    @transaction.atomic
    @action(detail=True, methods=["post"])
    def batal_lab(self, request, pk=None):
        try:
            screening = self.get_object()

            ScreeningPasienService.batal_lab(screening)

            return Response("Lab berhasil dibatalkan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_classes((IsAdminUser,))
    @transaction.atomic
    @action(detail=True, methods=["post"])
    def batal_radiologi(self, request, pk=None):
        try:
            screening = self.get_object()

            ScreeningPasienService.batal_radiologi(screening)

            return Response("Radiologi berhasil dibatalkan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_classes((IsAdminUser,))
    @transaction.atomic
    @action(detail=True, methods=["post"])
    def batal_ekg(self, request, pk=None):
        try:
            screening = self.get_object()

            ScreeningPasienService.batal_ekg(screening)

            return Response("EKG berhasil dibatalkan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_classes((IsAdminUser,))
    @transaction.atomic
    @action(detail=True, methods=["post"])
    def batal_kartu_kuning(self, request, pk=None):
        try:
            screening = self.get_object()

            ScreeningPasienService.batal_kartu_kuning(screening)

            return Response("Kartu Kuning berhasil dibatalkan!")
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            return Response(str(ex), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReportViewSet(viewsets.ViewSet):
    # @action(detail=False, methods=["get"])
    # def laporan_pendaftaran(self, request, pk=None):
    #     if request.query_params.get("tgl") is None:
    #         return Response("tgl wajib ada", status=status.HTTP_400_BAD_REQUEST)

    #     tgl = request.query_params.get("tgl")
    #     full_report = LaporanService.laporan_pendaftaran(tgl)

    #     return Response(full_report)

    # @action(detail=False, methods=["get"])
    # def download_laporan_pendaftaran(self, request, pk=None):

    #     workbook = LaporanService.laporan_pendaftaran_excel()

    #     response = HttpResponse(
    #         content=save_virtual_workbook(workbook),
    #         content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #     )
    #     response["Content-Disposition"] = "attachment; filename=LaporanPendaftaran.xlsx"
    #     return response

    @action(detail=False, methods=["get"])
    def laporan_kehadiran(self, request, pk=None):
        if request.query_params.get("tgl") is None:
            return Response("tgl wajib ada", status=status.HTTP_400_BAD_REQUEST)

        tgl = request.query_params.get("tgl")
        full_report = LaporanService.laporan_kehadiran(tgl)

        return Response(full_report)

    # @action(detail=False, methods=["get"])
    # def download_laporan_kehadiran(self, request, pk=None):

    # workbook = LaporanService.laporan_kehadiran_excel()

    # response = HttpResponse(
    #     content=save_virtual_workbook(workbook),
    #     content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    # )
    # response["Content-Disposition"] = "attachment; filename=LaporanKehadiran.xlsx"
    # return response

    @action(detail=False, methods=["get"])
    def laporan_screening(self, request, pk=None):
        if request.query_params.get("tgl") is None:
            return Response("tgl wajib ada", status=status.HTTP_400_BAD_REQUEST)

        tgl = request.query_params.get("tgl")
        full_report = LaporanService.laporan_screening(tgl)
        return Response(full_report)

        # @action(detail=False, methods=["get"])
        # def download_laporan_screening(self, request, pk=None):

        # workbook = LaporanService.laporan_screening_excel()

        # response = HttpResponse(
        #     content=save_virtual_workbook(workbook),
        #     content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        # )
        # response["Content-Disposition"] = "attachment; filename=LaporanScreening.xlsx"
        # return response


class KartuKuningViewSet(viewsets.ModelViewSet):
    queryset = KartuKuning.objects.all()
    serializer_class = KartuKuningSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        "pasien"
    ]  # kasih all ada error karena kolom perhatian itu array
