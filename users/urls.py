from django.urls import path

from users.views import UserRetrieveAPIView, UserUpdateAPIView

urlpatterns = [
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
]
