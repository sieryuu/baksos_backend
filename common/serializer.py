from django.contrib.auth.models import User
from rest_framework import serializers

DEFAULT_READ_ONLY_FIELDS = ['waktu_dibuat', 'dibuat_oleh', 'diperbaharui_oleh']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = DEFAULT_READ_ONLY_FIELDS
