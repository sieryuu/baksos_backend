from rest_framework import serializers

from common.serializer import DEFAULT_READ_ONLY_FIELDS

from .models import Penyakit, Puskesmas


class PenyakitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penyakit
        fields = '__all__'
        read_only_fields = DEFAULT_READ_ONLY_FIELDS


class PuskesmasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puskesmas
        fields = '__all__'
        read_only_fields = DEFAULT_READ_ONLY_FIELDS
