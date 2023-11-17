from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView

from users.models import User
from users.serializers import UserRetrieveSerializer, UserUpdateSerializer, UserCreateSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.data['password'])
        user.save()
