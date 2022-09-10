from django.shortcuts import render
from rest_framework import viewsets

from referensi.models import Penyakit, Puskesmas
from referensi.serializer import PenyakitSerializer, PuskesmasSerializer


# Create your views here.
class PenyakitViewSet(viewsets.ModelViewSet):
    queryset = Penyakit.objects.all()
    serializer_class = PenyakitSerializer

class PuskesmasViewSet(viewsets.ModelViewSet):
    queryset = Puskesmas.objects.all()
    serializer_class = PuskesmasSerializer