from rest_framework import serializers

from .models import Penyakit, Puskesmas


class PenyakitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penyakit
        fields = '__all__'


class PuskesmasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puskesmas
        fields = '__all__'
