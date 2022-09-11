from django.shortcuts import render
from rest_framework import viewsets

from referensi.models import Penyakit, Puskesmas
from referensi.serializer import PenyakitSerializer, PuskesmasSerializer
from django_filters import rest_framework as filters

# Create your views here.
class PenyakitViewSet(viewsets.ModelViewSet):
    queryset = Penyakit.objects.all()
    serializer_class = PenyakitSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = "__all__"


class PuskesmasViewSet(viewsets.ModelViewSet):
    queryset = Puskesmas.objects.all()
    serializer_class = PuskesmasSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = "__all__"
