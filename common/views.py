from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.decorators import action
from common.serializer import UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def get_user_permission(self, request, pk=None):
        user: User = self.get_object()
        return Response(user.get_all_permissions())
