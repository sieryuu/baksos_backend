from rest_framework import serializers
from .models import Pasien
from django.core.validators import FileExtensionValidator
class PasienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasien

class ImportPasienSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])