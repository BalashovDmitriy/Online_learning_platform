from rest_framework.generics import RetrieveAPIView, UpdateAPIView

from users.models import User
from users.serializers import UserRetrieveSerializer, UserUpdateSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
