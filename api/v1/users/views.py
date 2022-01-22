from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import User
from . import serializer


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response({"status": "Success",
                         "Users": serializer.data})


class UserRegister(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializer.RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        self.perform_create(serializer_class)
        headers = self.get_success_headers(serializer_class.data)
        return Response({"status": "Sucesss",
                         "message": "User created!",
                         "User": serializer_class.data},
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs.get('pk'))

    # we override this method for a custom response
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        if not queryset:
            return ""
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer(instance)
        if not instance:
            return user_not_found()

        return Response({"status": "Success",
                         "message:": "User found",
                         "User": serializer_class.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        if not instance:
            return user_not_found()

        serializer_class = self.get_serializer(instance, data=request.data, partial=partial)
        serializer_class.is_valid(raise_exception=True)
        self.perform_update(serializer_class)

        return Response({"status": "Success",
                         "message": "User Updated",
                         "User": serializer_class.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return user_not_found()

        self.perform_destroy(instance)
        return Response({"status": "Success",
                         "message": "User deleted"},
                        status=status.HTTP_202_ACCEPTED)


def user_not_found():
    return Response({"status": "Failed",
                     "message": "User not found"},
                    status=status.HTTP_204_NO_CONTENT)
