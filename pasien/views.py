from rest_framework import viewsets
from pasien.models import Pasien
from pasien.serializer import ImportPasienSerializer, PasienSerializer
from rest_framework.decorators import action
from pasien.services import pasien as PasienService
from django.http import HttpResponse
from openpyxl.writer.excel import save_virtual_workbook

# Create your views here.
class PasienViewSet(viewsets.ViewSet):
    queryset = Pasien.objects.all()
    serializer_class = PasienSerializer

    @action(detail=False, methods=['get'])
    def template(self, request, pk=None):
        workbook = PasienService.generate_import_template()
        response = HttpResponse(
            content=save_virtual_workbook(workbook),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=PasienTemplate.xlsx"
        return response

    @action(detail=False, methods=['post'])
    def import_pasien(self, request, pk=None):
        try:
            serializer = ImportPasienSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            PasienService.import_pasien(file=serializer.validated_data['file'])
            response = HttpResponse(
                content="Import File Sukses!",
            )
            return response
        except Exception as ex:
            raise ex

