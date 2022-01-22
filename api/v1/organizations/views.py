from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from organizations.models import Organization
from . import serializer


class OrganizationListCreate(ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = serializer.OrganizationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        self.perform_create(serializer_class)
        headers = self.get_success_headers(serializer_class.data)
        return Response({"status": "Success",
                         "message": "Organization created!",
                         "Organization": serializer_class.data},
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer_class = self.get_serializer(queryset, many=True)
        return Response({"status": "Success",
                         "Organizations": serializer_class.data})


class OrganizationRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.filter(id=self.kwargs.get('pk'))

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
            return organization_not_found()

        return Response({"status": "Success",
                         "message:": "Organization found",
                         "Organization": serializer_class.data})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not instance:
            return organization_not_found()

        serializer_class = self.get_serializer(instance, data=request.data, partial=partial)
        serializer_class.is_valid(raise_exception=True)
        self.perform_update(serializer_class)

        return Response({"status": "Success",
                         "message": "Organization Updated",
                         "data": serializer_class.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return organization_not_found()

        self.perform_destroy(instance)
        return Response({"status": "Success",
                         "message": "Organization deleted"},
                        status=status.HTTP_202_ACCEPTED)


def organization_not_found():
    return Response({"status": "Failed",
                     "message": "Organization not found"},
                    status=status.HTTP_204_NO_CONTENT)
