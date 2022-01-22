from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from . import serializer


class UserListCreate(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "Sucess",
                         "Users": serializer.data})
