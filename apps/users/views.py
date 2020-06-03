from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser
)

from rest_framework.response import Response

from apps.users.models import User
from apps.users.permissions import MixedPermissionModelViewSet
from apps.users.serializers import UserSerializer, UserWriteSerializer





class UserViewSet(MixedPermissionModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes_by_action = {
        'retrieve': [AllowAny],
        'list': [AllowAny],
        'create': [IsAuthenticated, IsAdminUser],
        'update': [IsAuthenticated],
        'partial_update': [IsAuthenticated],
        'destroy': [IsAuthenticated, IsAdminUser],
        'profile': [IsAuthenticated],
        'login': [AllowAny],
        'register': [IsAuthenticated, IsAdminUser],
        'password_reset': [AllowAny],
        'password_change': [AllowAny],
    }

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)


    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return UserWriteSerializer
