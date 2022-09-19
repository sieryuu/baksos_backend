from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.decorators import action
from common.serializer import UserSerializer
from django_filters import rest_framework as filters
from crum import get_current_user

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = "__all__"

    @action(detail=False, methods=["get"])
    def get_user_permission(self, request, pk=None):
        user: User = get_current_user()

        user_dict = model_to_dict(
            user,
            [
                "id,",
                "is_superuser",
                "username",
                "first_name",
                "last_name",
                "email",
                "is_staff",
                "is_active",
                "groups",
            ],
        )
        groups = []
        for x in user_dict["groups"]:
            groups.append(model_to_dict(x, ["name", "id"]))
        user_dict["groups"] = groups

        return Response({"user": user_dict, "permissions": user.get_all_permissions()})
