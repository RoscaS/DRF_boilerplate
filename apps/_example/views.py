from rest_framework import viewsets

from apps._example.models import Example
from apps._example.serializers import ExampleSerializer


class ExampleViewSet(viewsets.ModelViewSet):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, args, kwargs)
